from typing import Any
import pandas as pd


def add_row(balances: pd.DataFrame, row: list[Any]):
    balances.loc[len(balances.index)] = row  # type: ignore
