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
        date, st.sidebar.date_input("Date from", date.today() - timedelta(days=2 + 6))
    )


def date_to():
    return cast(
        date, st.sidebar.date_input("Date to", date.today() - timedelta(days=2))
    )


def step_to_price_ratio():
    return (
        st.sidebar.slider(
            "Step to price ratio, %",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="How much price should change in %, to make an action",
        )
        / 100.0
    )


def order_leverage():
    return st.sidebar.slider(
        "Order Leverage",
        min_value=1.0,
        max_value=100.0,
        value=2.0,
        step=1.0,
    )


def order_quantity():
    return st.sidebar.number_input(
        "Order Quantity",
        min_value=0.001,
        max_value=1000.0,
        value=0.01,
        step=0.001,
        format="%0.3f",
    )


def tp_to_entry_price_ratio():
    return (
        st.sidebar.slider(
            "Take Profit to entry price ratio, %",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
        )
        / 100.0
    )


def sl_to_entry_price_ratio():
    return (
        st.sidebar.slider(
            "Stop Loss to entry price ratio, %",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
        )
        / -100.0
    )


def inverted():
    return st.sidebar.checkbox(
        "Inverted",
        value=False,
        help="Change BUY and SELL sides in algorythm",
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


def positions_sort_timestamp_column():
    return cast(
        str,
        st.radio(
            "Positions sorted by:",
            ("entry_timestamp", "exit_timestamp"),
            horizontal=True,
        ),
    )
