from datetime import date, timedelta
from typing import cast
import streamlit as st
from binance.binance_k_line_loader import BINANCE_SYMBOLS


def symbol():
    return cast(
        str,
        st.sidebar.selectbox(
            "Символ", options=BINANCE_SYMBOLS, index=BINANCE_SYMBOLS.index("ETHUSDT")
        ),
    )


def date_from():
    return cast(
        date, st.sidebar.date_input("Дата с", date.today() - timedelta(days=2 + 6))
    )


def date_to():
    return cast(
        date, st.sidebar.date_input("Дата по", date.today() - timedelta(days=2))
    )


def price_step_ratio():
    return (
        st.sidebar.slider(
            "Шаг цены, %",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="На сколько должна измениться цена, что бы бот сделал действие",
        )
        / 100.0
    )


def take_profit_to_price_ratio():
    return (
        st.sidebar.slider(
            "Take Profit, %",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="Сколко Take Profit составляет процентов от цены",
        )
        / 100.0
    )


def stop_loss_to_price_ratio():
    return (
        st.sidebar.slider(
            "Stop Loss, %",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="Сколко Stop Loss составляет процентов от цены",
        )
        / 100.0
    )


def inverted():
    return st.sidebar.checkbox(
        "Инвертировать",
        value=False,
        help="Поменять местами покупку и продажу в алгоритме",
    )


def symbol_ask_bid_price_difference():
    return st.sidebar.number_input("Разница цены купли-проажи", value=0.01)
