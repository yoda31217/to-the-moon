from typing import cast
import altair as alt  # pyright: ignore [[reportUnknownMemberType]
import pandas as pd
from streamlit.delta_generator import DeltaGenerator

from simulator.utils.series import TypedSeries


# TODO fix types
def line(
    tab: DeltaGenerator,
    data_frame: pd.DataFrame,
    timestamp_column_name: str,
    value_column_name: str,
    value_label: str,
    samples_count: int = 10_000,
    is_cumulative: bool = False,
):
    value_series: TypedSeries[float] = cast(
        TypedSeries[float], data_frame[value_column_name]
    )

    formatted_data_frame = pd.DataFrame(
        {
            "Date Time": data_frame[timestamp_column_name],
            value_column_name: (
                value_series.cumsum() if is_cumulative else value_series
            ),
        }
    )

    tab.altair_chart(
        alt.Chart(formatted_data_frame)  # type: ignore
        .mark_line(interpolate="step-after")  # type: ignore
        .encode(
            x=alt.X(
                shorthand="Date Time" + ":T",  # type: ignore
                title="Date Time",  # type: ignore
                axis=alt.Axis(format="%y-%m-%d %H:%M"),  # type: ignore
            ),
            y=alt.Y(
                shorthand=value_column_name + ":Q",  # type: ignore
                title=value_label,  # type: ignore
                scale=alt.Scale(zero=False),  # type: ignore
            ),
            color=altair_value("#4dabf5"),
        )
        .transform_sample(samples_count),
        use_container_width=True,
    )


def bars(
    tab: DeltaGenerator,
    data_frame: pd.DataFrame,
    timestamp_column_name: str,
    value_column_name: str,
    value_label: str,
    samples_count: int = 10_000,
):
    formatted_data_frame = pd.DataFrame(
        {
            "Date Time": data_frame[timestamp_column_name],
            value_column_name: data_frame[value_column_name],
        }
    )

    tab.altair_chart(
        alt.Chart(formatted_data_frame)  # type: ignore
        .mark_bar()  # type: ignore
        .encode(
            x=alt.X(
                shorthand="Date Time" + ":T",  # type: ignore
                title="Date Time",  # type: ignore
                axis=alt.Axis(format="%y-%m-%d %H:%M"),  # type: ignore
            ),
            y=alt.Y(
                shorthand=value_column_name + ":Q",  # type: ignore
                title=value_label,  # type: ignore
            ),
            color=alt.condition(  # pyright: ignore [reportUnknownMemberType]
                alt.datum[value_column_name] > 0,
                altair_value("#4dabf5"),
                altair_value("#ff784e"),
            ),
        )
        .transform_sample(samples_count),
        use_container_width=True,
    )


def histogram(
    tab: DeltaGenerator,
    data_frame: pd.DataFrame,
    value_column_name: str,
    value_label: str,
    entities_label: str,
):
    tab.altair_chart(
        alt.Chart(data_frame)  # type: ignore
        .mark_bar()  # type: ignore
        .encode(
            x=alt.X(
                shorthand=value_column_name + ":Q",  # type: ignore
                title=value_label,  # type: ignore
                bin=True,  # type: ignore
            ),
            y=alt.Y(
                shorthand="count()",  # type: ignore
                title=entities_label + " Count",  # type: ignore
            ),
            color=altair_value("#4dabf5"),
        ),
        use_container_width=True,
    )


def altair_value(value: str) -> dict[str, str]:
    return cast(
        dict[str, str], alt.value(value)  # pyright: ignore [reportUnknownMemberType]
    )
