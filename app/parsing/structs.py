import dataclasses as dc
from datetime import datetime

from app.user.structs import ExpenseGroups


@dc.dataclass()
class Expense:
    name: str
    qnt: int | None
    unt_cost: float | None
    total_cost: float
    group_name: ExpenseGroups
    auto_expense: bool
    created_at: datetime

    def __post_init__ (self) -> None:
        if self.qnt is not None:
            self.qnt = int(self.qnt)

        if self.unt_cost is not None:
            self.unt_cost = float(self.unt_cost)

        self.total_cost = float(self.total_cost)
        self.group_name = ExpenseGroups(self.group_name)

    def to_csv (self) -> None:
        return {
            "name": self.name,
            "qnt": self.qnt,
            "unt_cost": self.unt_cost,
            "total_cost": self.total_cost,
            "group_name": self.group_name.value,
            "auto_expense": self.auto_expense,
            "created_at": self.created_at.strftime("%d/%m/%Y"),
        }
