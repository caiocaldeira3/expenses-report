from collections.abc import Iterable

from app.parsing.methods import (discriminate_expenses, get_file_ocr,
                                 get_pdf_file)


def parse_expense (file_name: str, groups: Iterable[str]) -> None:
    file_content = get_pdf_file(file_name)
    file_ocr = get_file_ocr(file_content)

    return discriminate_expenses(file_ocr, groups)
