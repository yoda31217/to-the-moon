from datetime import date

import streamlit as st
from simulator.backtester.backtester import Backtester
from simulator.binance import binance_ticker_repository
from simulator.market.market_ticker import MarketTikersDataFrame
from simulator.report.report_bot import ReportBotConfig


@st.cache_data
def test(
    symbol: str,
    date_from: date,
    date_to: date,
    bid_ask_spread: float,
    report_bot_config: ReportBotConfig,
):
    if (date_to - date_from).days > 31:
        raise Exception(f"Date 'to' - 'from' interval should be <= 31 days.")

    tickers = load_tickers(symbol, date_from, date_to, bid_ask_spread)
    return backtester_test(report_bot_config, tickers)


@st.cache_data
def backtester_test(report_bot_config: ReportBotConfig, tickers: MarketTikersDataFrame):
    bot = report_bot_config["bot_constructor"](report_bot_config["bot_config"])
    return Backtester(tickers).test(bot)


@st.cache_data
def load_tickers(symbol: str, date_from: date, date_to: date, bid_ask_spread: float):
    return binance_ticker_repository.load_tickers(
        symbol, date_from, date_to, bid_ask_spread
    )
