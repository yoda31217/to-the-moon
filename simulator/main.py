from datetime import date, timedelta
from typing import cast

import streamlit as st
from binance.binance_k_line_loader import BINANCE_SYMBOLS, load_binance_k_lines
from binance.binance_tick_loader import load_binance_ticks
from bot.bot_0_strategy import Bot0Strategy
from report.report import (input_date_from_widget, input_date_to_widget,
                           input_inverted_widget,
                           input_price_step_ratio_widget,
                           input_symbol_ask_bid_price_difference_widget,
                           input_symbol_widget, report_profit_chart,
                           report_summary, report_ticks_chart,
                           text_description)
from trade.trade_simulator import TradeSimulator

st.set_page_config(
    page_title=f"Симулятор торговли бота на крипто бирже",
    initial_sidebar_state="expanded",
)

st.header(f"Симулятор торговли крипто бота")
text_description()

st.sidebar.title("Опции")
st.sidebar.header("Рынок")
st.sidebar.markdown("**Биржа: Binance**")
symbol: str = input_symbol_widget()
date_from: date = input_date_from_widget()
date_to: date = input_date_to_widget()
symbol_ask_bid_price_difference = input_symbol_ask_bid_price_difference_widget()
st.sidebar.header("Bot")
st.sidebar.markdown("**Название: Bot0**")
price_step_ratio = input_price_step_ratio_widget()
inverted = input_inverted_widget()

try:
    strategy = Bot0Strategy(price_step_ratio, inverted)
    k_lines = load_binance_k_lines(symbol, date_from, date_to)
    ticks = load_binance_ticks(k_lines, symbol_ask_bid_price_difference)
    result = TradeSimulator(ticks).simulate(strategy)

    report_summary(symbol, date_from, date_to, strategy, result)
    report_ticks_chart(ticks)
    report_profit_chart(result)

except Exception as e:
    st.error(f"Ошибка: {str(e)}", icon="🚨")
