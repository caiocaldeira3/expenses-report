import matplotlib.pyplot as plt
import pandas as pd

from app import config
from app.parsing.structs import Expense
from app.user.structs import Profile


def save_expenses (expenses: list[Expense]) -> bool:
    df = pd.DataFrame( exp.to_csv() for exp in expenses )
    df.to_csv(
        config.PROFILE_PATH / "expenses-report.csv", mode="a",
        index=False, header=False
    )

def plot_expenses_distribution (profile: Profile) -> None:
    df = pd.read_csv(config.PROFILE_PATH / "expenses-report.csv")

    fig, ax = plt.subplots(figsize=(8, 4))

    dist_expenses = list(zip(*(
        ( group_name.value, df[df.group_name == group_name].total_cost.sum() )
        for group_name in profile.expenses_groups
    )))

    ax.set_ylabel("Expenses Distribution")
    ax.bar(dist_expenses[0], dist_expenses[1], label="Cumulative Cost")

    fig.savefig(config.GRAPHS_PATH / "exp-dist.png", dpi=300, transparent=False)
