from datetime import date

import streamlit as st
from backtester.backtester import Backtester
from binance import binance_ticker_repository
from bot.bot_one_step_order import BotOneStepOrder
import report.report_input as report_input
import report.report_result as report_result


def build_report():
    st.set_page_config(
        page_title=f"To the Moon: crypto trading bot Backtester",
        page_icon="🌕",
        initial_sidebar_state="expanded",
    )

    st.title(f"🌕 To the Moon")
    st.caption(f"Crypto trading bot Backtester")

    st.sidebar.title("Options")

    st.sidebar.header("Market")
    st.sidebar.markdown("**Exchange: Binance**")
    st.sidebar.markdown("**Market: USDⓈ-M Futures**")
    symbol: str = report_input.symbol()
    date_from: date = report_input.date_from()
    date_to: date = report_input.date_to()
    bid_ask_spread = report_input.bid_ask_spread()

    st.sidebar.header("Bot")
    st.sidebar.markdown("**Name: BotOneStepOrder**")
    step_to_price_ratio = report_input.step_to_price_ratio()
    tp_to_entry_price_ratio = report_input.tp_to_entry_price_ratio()
    sl_to_entry_price_ratio = report_input.sl_to_entry_price_ratio()
    inverted = report_input.inverted()

    bot = BotOneStepOrder(
        step_to_price_ratio, tp_to_entry_price_ratio, sl_to_entry_price_ratio, inverted
    )
    tickers = binance_ticker_repository.load_tickers(
        symbol, date_from, date_to, bid_ask_spread
    )
    result = Backtester(tickers).test(bot)

    report_result.summary(symbol, date_from, date_to, bot, result)
    report_result.tickers_chart(tickers)
    report_result.balance_chart(result)
    report_result.positions_table(result.positions)
