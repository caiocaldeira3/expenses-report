import dataclasses as dc


@dc.dataclass()
class Expense:
    name: str
    qnt: int | None
    unt_cost: float | None
    total_cost: float

    def __post_init__ (self) -> None:
        if self.qnt is not None:
            self.qnt = int(self.qnt)

        if self.unt_cost is not None:
            self.unt_cost = float(self.unt_cost)

        if self.total_cost is not None:
            self.total_cost = float(self.total_cost)
