import altair as alt
import pandas as pd
import streamlit as st


def draw_line_chart(
    data_frame: pd.DataFrame,
    timestamp_column_name: str,
    value_column_name: str,
    value_label: str,
    samples_count: int = 10000,
):
    formatted_data_frame = pd.DataFrame(
        {
            "Date Time": data_frame[timestamp_column_name],
            value_label: data_frame[value_column_name],
        }
    )

    st.altair_chart(
        alt.Chart(formatted_data_frame)  # type: ignore
        .mark_line()
        .encode(
            x=alt.X(
                shorthand="Date Time" + ":T",  # type: ignore
                title="Время",  # type: ignore
                axis=alt.Axis(format="%y-%m-%d %H:%M"),  # type: ignore
            ),
            y=alt.Y(
                shorthand=value_label + ":Q",  # type: ignore
                title=value_label,  # type: ignore
                scale=alt.Scale(zero=False),  # type: ignore
            ),
        )
        .transform_sample(samples_count),
        use_container_width=True,
    )
