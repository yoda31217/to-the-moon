from datetime import date

import streamlit as st
from report import report_backtester, report_bot
import report.report_input as report_input
import report.report_result as report_result
from utils import gits


def build_report(bot_repository: report_bot.ReportBotRepository):
    st.set_page_config(
        page_title=f"To the Moon: crypto trading bot Backtester",
        page_icon="🌕",
        initial_sidebar_state="expanded",
    )

    st.title(f"🌕 To the Moon")
    st.caption(f"Crypto trading bot Backtester.")

    st.sidebar.title("Options")

    st.sidebar.header("Market")
    st.sidebar.markdown("**Exchange: Binance**")
    st.sidebar.markdown("**Market: USDⓈ-M Futures**")
    symbol: str = report_input.symbol()
    date_from: date = report_input.date_from()
    date_to: date = report_input.date_to()
    bid_ask_spread = report_input.bid_ask_spread()

    st.sidebar.header("Bot")
    report_bot_config = report_bot.config(bot_repository)

    backtester_result = report_backtester.test(
        symbol, date_from, date_to, bid_ask_spread, report_bot_config
    )

    (
        summary_tab,
        positions_tab,
        positions_pnl_tab,
        balance_tab,
        tickers_tab,
        bot_tab,
    ) = st.tabs(["Summary", "Positions", "Positions PNL", "Balance", "Tickers", "Bot"])

    report_result.summary(symbol, date_from, date_to, backtester_result, summary_tab)
    report_result.pnl_chart(backtester_result, positions_pnl_tab)
    report_result.positions_table(backtester_result.positions, positions_tab)
    report_result.balances_chart(backtester_result, balance_tab)
    report_result.tickers_chart(backtester_result.tickers, tickers_tab)
    report_result.bot_summary(backtester_result.bot, bot_tab)

    st.divider()
    st.caption(
        f"""
            Version: {gits.get_version()}
            
            2023 🌕 To the Moon
        """
    )
