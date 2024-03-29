import dataclasses as dc
import json
import os
from collections.abc import Iterable

from app import config
from app.parsing.structs import Expense
from app.user.structs import ExpenseGroups, Profile


def load_profile () -> Profile | None:
    if not os.path.exists(config.PROFILE_PATH / "profile.json"):
        raise ValueError("profile not setup")

    with open(config.PROFILE_PATH / "profile.json") as profile_file:
        user = Profile(**json.load(profile_file))

    return user

def create_profile (
    name: str = "usr", expenses_group: Iterable[ExpenseGroups] = list(ExpenseGroups),
    expected_expenses: float | None = None
) -> Profile:
    user = Profile(name, expenses_group, expected_expenses)

    with open(config.PROFILE_PATH / "profile.json", "w") as profile_file:
        json.dump(user.__dict__, profile_file, indent=4)

    with open(config.PROFILE_PATH / "expenses-report.csv", "w") as report_file:
        report_file.write(
            ",".join( field.name for field in dc.fields(Expense) if field.init ) + "\n"
        )

    return user

def ensure_profile () -> None:
    try:
        return load_profile()

    except Exception:
        if not os.path.exists(config.PROFILE_PATH):
            os.makedirs(config.PROFILE_PATH)

        if not os.path.exists(config.EXPENSES_PATH):
            os.makedirs(config.EXPENSES_PATH)

        username = input("choose username: ") or "usr"
        groups = (
            input("choose expenses group: [empty for default] ")
            or list(ExpenseGroups)
        )
        expected_expenses = input("expected monthly expenses: ") or None

        return create_profile(username, groups, expected_expenses)
