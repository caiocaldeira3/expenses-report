import dataclasses as dc
from collections.abc import Iterable
from enum import Enum


class Expenses (str, Enum):
    GROCERIES: str = "groceries"
    UTILITIES: str = "utility-bills"
    HYGIENE: str = "hygiene"
    GAMES: str = "games"
    UBER: str = "uber"
    IFOOD: str = "ifood"
    EXTRAS: str = "extras"

@dc.dataclass()
class Profile:
    name: str
    expenses_groups: Iterable[Expenses]
    expected_expenses: float | None
    temporary_expenses: bool = dc.field(default=False)

    def __post_init__ (self) -> None:
        if self.expected_expenses is not None:
            self.expected_expenses = float(self.expected_expenses)

        self.expenses_groups = [
            Expenses(exp) for exp in self.expenses_groups
        ]
