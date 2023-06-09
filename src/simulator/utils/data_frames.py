from typing import TypeVar, cast
import pandas as pd

DF = TypeVar("DF", bound=pd.DataFrame)


def concat(data_frames: list[DF]) -> DF:
    return cast(DF, pd.concat(data_frames))  # pyright: ignore [reportUnknownMemberType]


def sort_by(data_frame: DF, column: str) -> DF:
    return data_frame.sort_values(  # pyright: ignore [reportUnknownMemberType]
        by=[column]
    )
