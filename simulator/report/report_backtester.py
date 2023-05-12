from datetime import date

import pandas as pd
from backtester.backtester import Backtester
from binance import binance_ticker_repository
from bot.bot_one_step_order import BotOneStepOrder


def test(
    symbol: str, date_from: date, date_to: date, bid_ask_spread: float, bot_config: dict
):
    tickers = load_tickers(symbol, date_from, date_to, bid_ask_spread)
    return backtester_test(bot_config, tickers)


def backtester_test(bot_config: dict, tickers: pd.DataFrame):
    bot = BotOneStepOrder(bot_config)
    return Backtester(tickers).test(bot)


def load_tickers(symbol: str, date_from: date, date_to: date, bid_ask_spread: float):
    return binance_ticker_repository.load_tickers(
        symbol, date_from, date_to, bid_ask_spread
    )
