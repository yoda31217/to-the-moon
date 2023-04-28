from datetime import date
import pandas as pd

import streamlit as st
import report.report_chart as report_chart
from backtester.backtester_result import BacktesterResult

from bot.bot import Bot


def summary(
    symbol: str,
    date_from: date,
    date_to: date,
    bot: Bot,
    result: BacktesterResult,
):
    st.subheader(f"Summary")
    st.table(
        pd.DataFrame(
            {
                "Property": [
                    "Exchange",
                    "Symbol",
                    "Test interval",
                    "Bot",
                    "Average ticker price change",
                    "Positions count",
                    "Positions count / day",
                    "Positions average price margin",
                    "Positions average quantity",
                    "Positions average initial margin",
                    "Positions average PNL",
                    "Positions average ROE",
                    "Positions initial margin sum",
                    "Balance",
                ],
                "Value": [
                    "Binance",
                    symbol,
                    "{} - {} ({:.1f} days)".format(
                        date_from, date_to, result.get_interval_days()
                    ),
                    str(bot),
                    "{:.2f} $".format(result.get_average_tickers_price_change()),
                    "{:,}".format(result.get_positions_count()),
                    "{:,.2f}".format(
                        result.get_positions_count() / result.get_interval_days()
                    ),
                    "{:,.2f}$ (abosolute)".format(
                        result.get_positions_average_price_margin()
                    ),
                    "1",
                    "{:,.2f} $".format(result.get_positions_average_initial_margin()),
                    "{:,.2f} $".format(result.get_positions_average_pnl()),
                    "{:,.2f} %".format(result.get_positions_average_roe() * 100.0),
                    "{:,.2f} $".format(result.get_positions_initial_margin_sum()),
                    "{:,.2f} $".format(result.get_positions_balance()),
                ],
            }
        )
    )


def tickers_chart(tickers: pd.DataFrame):
    st.subheader(f"Ask Price")
    report_chart.line(
        tickers,
        "timestamp",
        "ask_price",
        "Ask Price, $",
        samples_count=1_000,
    )


def balance_chart(result: BacktesterResult):
    st.subheader(f"Balance")
    if result.get_positions_count() > 0:
        report_chart.line(
            result.positions,
            "entry_timestamp",
            "balance",
            "Balance, $",
            samples_count=10_000,
        )
    else:
        st.text("There were NO positions! 😕")
