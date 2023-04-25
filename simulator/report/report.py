from datetime import date

import streamlit as st
from binance.binance_k_line_loader import load_binance_k_lines
from binance.binance_tick_loader import load_binance_ticks
from bot.bot_one_step_order import BotOneStepOrder
import report.report_input as report_input
import report.report_result as report_result
from trade.trade_simulator import TradeSimulator


def build_report():
    st.set_page_config(
        page_title=f"Симулятор торговли бота на крипто бирже",
        initial_sidebar_state="expanded",
    )

    st.header(f"Симулятор торговли крипто бота")
    with st.expander("Описание", expanded=False):
        st.write(
            """
                Привет!
                
                Проект открытый. Вот
                исходники проекта на [GitHub](https://github.com/yoda31217/to-the-moon)
                и примеры 
                [Бота](https://github.com/yoda31217/to-the-moon/blob/main/simulator/bot).
            """
        )

    st.sidebar.title("Опции")

    st.sidebar.header("Рынок")
    st.sidebar.markdown("**Биржа: Binance**")
    symbol: str = report_input.symbol()
    date_from: date = report_input.date_from()
    date_to: date = report_input.date_to()
    symbol_ask_bid_price_difference = report_input.symbol_ask_bid_price_difference()

    st.sidebar.header("Bot")
    st.sidebar.markdown("**Название: Bot0**")
    price_step_ratio = report_input.price_step_ratio()
    inverted = report_input.inverted()

    bot = BotOneStepOrder(price_step_ratio, inverted)
    k_lines = load_binance_k_lines(symbol, date_from, date_to)
    ticks = load_binance_ticks(k_lines, symbol_ask_bid_price_difference)
    result = TradeSimulator(ticks).simulate(bot)

    report_result.summary(symbol, date_from, date_to, bot, result)
    report_result.ticks_chart(ticks)
    report_result.profit_chart(result)
