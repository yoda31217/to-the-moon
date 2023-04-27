from datetime import date

import streamlit as st
from backtester.backtester import BackTester
from binance import binance_ticker_repository
from bot.bot_one_step_order import BotOneStepOrder
import report.report_input as report_input
import report.report_result as report_result


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
                [Ботов](https://github.com/yoda31217/to-the-moon/blob/main/simulator/bot).
            """
        )

    st.sidebar.title("Опции")

    st.sidebar.header("Рынок")
    st.sidebar.markdown("**Биржа: Binance**")
    symbol: str = report_input.symbol()
    date_from: date = report_input.date_from()
    date_to: date = report_input.date_to()
    bid_ask_spread = report_input.symbol_ask_bid_price_difference()

    st.sidebar.header("Bot")
    st.sidebar.markdown("**Название: BotOneStepOrder**")
    price_step_ratio = report_input.price_step_ratio()
    take_profit_to_price_ratio = report_input.take_profit_to_price_ratio()
    stop_loss_to_price_ratio = report_input.stop_loss_to_price_ratio()
    inverted = report_input.inverted()

    bot = BotOneStepOrder(
        price_step_ratio, take_profit_to_price_ratio, stop_loss_to_price_ratio, inverted
    )
    ticks = binance_ticker_repository.load_tickers(
        symbol, date_from, date_to, bid_ask_spread
    )
    result = BackTester(ticks).simulate(bot)

    report_result.summary(symbol, date_from, date_to, bot, result)
    # st.dataframe(result.transactions)
    report_result.ticks_chart(ticks)
    report_result.profit_chart(result)
