import json
from datetime import datetime
from pathlib import Path

import google.generativeai as genai
import img2pdf
import magic
import regex as re
from google.api_core.client_options import ClientOptions
from google.cloud import documentai as doai

from app import config
from app.parsing.structs import Expense
from app.user.structs import Profile


def get_pdf_file (file_path: str | Path) -> bytes:
    og_mime = magic.from_file(
        config.EXPENSES_PATH / file_path, mime=True
    )

    if og_mime[ : 5 ] == "image":
        return img2pdf.convert(config.EXPENSES_PATH / file_path)

    elif og_mime != config.PDF_MIME_TYPE:
        raise ValueError("Invalid file format")

    with open(config.EXPENSES_PATH / file_path, "rb") as f:
        content = f.read()

    return content

def get_file_ocr (image_content: bytes) -> str:
    docapi = doai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=config.LOCATION + "-documentai.googleapis.com",
            credentials_file=config.DOAI_KEY_PATH
        ),
    )

    RESOURCE_NAME = docapi.processor_path(
        config.PROJECT_ID, config.LOCATION, config.PROCESSOR_ID
    )

    raw_document = doai.RawDocument(
        content=image_content, mime_type=config.PDF_MIME_TYPE
    )

    # Configure the process request
    request = doai.ProcessRequest(name=RESOURCE_NAME, raw_document=raw_document)

    return docapi.process_document(request=request).document.text

genai.configure(api_key=config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")
REMOVE_WEB_CHARACTERS = re.compile(r"`|\n|json")
REPLACE_CURRENCY_COMMA_FOR_DOT = re.compile(r"([0-9]+),([0-9]+)")

def discriminate_expenses (
    expense_ocr: str, user: Profile
) -> dict[str, list[Expense]]:
    response = model.generate_content(
        "Discriminate the following billing items between the given expenses groups:" +
        "\n".join(
            f" * {group.value}" for group in user.expenses_groups
        ) + "\n" +
        "As a json file that follows this structure:\n" +
        """
        [
            {
                "name":         the item name,
                "qnt":          the item quantity none if undecidable,
                "unt_cost":     the item unity cost, none if undecidable,
                "total_cost":   the item total cost,
                "group_name":   the item group name
            }
        ] ...
        """ +
        expense_ocr
    )

    parsed_text = REMOVE_WEB_CHARACTERS.sub(
        "", response.candidates[0].content.parts[0].text
    )
    parsed_text = REPLACE_CURRENCY_COMMA_FOR_DOT.sub(
        r"\g<1>.\g<2>", parsed_text
    )

    try:
        js_resp: list[dict[str, str | float]] = json.loads(parsed_text)

        return [
            Expense(
                auto_expense=True,
                created_at=datetime.now(),
                **exp
            ) for exp in js_resp
        ], response

    except json.JSONDecodeError:
        print("it was not possible to load parsed response as json")
        print(parsed_text)

        return parsed_text, response

    except Exception:
        print("generic exception")

        return parsed_text, response

def parse_expense (file_name: str, user: Profile) -> None:
    file_content = get_pdf_file(file_name)
    file_ocr = get_file_ocr(file_content)

    return discriminate_expenses(file_ocr, user)
