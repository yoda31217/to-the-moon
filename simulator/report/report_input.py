from datetime import date, timedelta
from typing import cast
import streamlit as st


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


def pnl_chart_type():
    return st.radio(
        "PNL chart type",
        ("PNL sum (cumulative, agregated)", "PNL"),
        horizontal=True,
        label_visibility="collapsed",
    )
