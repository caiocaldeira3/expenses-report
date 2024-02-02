import dataclasses as dc
from collections.abc import Iterable
from enum import Enum


class ExpenseGroups (str, Enum):
    GROCERIES: str = "groceries"
    HYGIENE: str = "hygiene"
    GAMES: str = "games"
    EXTRAS: str = "extras"

@dc.dataclass()
class Profile:
    name: str
    expenses_groups: Iterable[ExpenseGroups]
    expected_expenses: float | None
    temporary_expenses: bool = dc.field(default=False)

    def __post_init__ (self) -> None:
        if self.expected_expenses is not None:
            self.expected_expenses = float(self.expected_expenses)

        self.expenses_groups = [
            ExpenseGroups(exp) for exp in self.expenses_groups
        ]
