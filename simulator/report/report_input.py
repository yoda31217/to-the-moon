from datetime import date, timedelta
from typing import cast
import streamlit as st
from streamlit.delta_generator import DeltaGenerator


def symbol():
    return cast(
        str,
        st.sidebar.selectbox("Symbol", options=["ETHUSDT", "BTCUSDT"], index=0),
    )


def date_from():
    return cast(
        date, st.sidebar.date_input("Date from", date.today() - timedelta(days=3 + 6))
    )


def date_to():
    return cast(
        date, st.sidebar.date_input("Date to", date.today() - timedelta(days=3))
    )


def bid_ask_spread():
    return st.sidebar.number_input("Bid-Ask spread", value=0.01)


def pnl_chart_type(tab: DeltaGenerator):
    return tab.radio(
        "PNL chart type",
        ("cumulative PNL sum", "PNL sum"),
        horizontal=True,
        label_visibility="collapsed",
    )


def balance_chart_type(tab: DeltaGenerator):
    return tab.radio(
        "Balance chart type",
        ("Available Balance", "Margin Balance"),
        horizontal=True,
        label_visibility="collapsed",
    )


def positions_sort_timestamp_column(key_prefix: str, tab: DeltaGenerator):
    return cast(
        str,
        tab.radio(
            "Positions sorted by:",
            ("entry_timestamp", "exit_timestamp"),
            horizontal=True,
            key=f"{key_prefix}_positions_sort_timestamp_column",
        ),
    )


def positions_chart_attribute(tab: DeltaGenerator):
    return cast(
        str,
        tab.selectbox(
            "Position(s) attribute",
            options=[
                "roe",
                "pnl",
                "initial_margin",
                "quantity",
                "price_margin",
                "exit_price",
                "entry_price",
                "side",
                "durarion_millis",
            ],
            index=0,
        ),
    )
