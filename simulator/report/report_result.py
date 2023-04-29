from datetime import date
from datetime import timedelta
import pandas as pd

import streamlit as st
from report import report_input
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
                    "Market",
                    "Symbol",
                    "Test interval",
                    "Bot",
                    "Tickers average price change",
                    "Tickers average interval",
                    "Positions count",
                    "Positions count / day",
                    "Positions average duration",
                    "Positions average price margin",
                    "Positions average quantity",
                    "Positions average initial margin",
                    "Positions average PNL",
                    "Positions average ROE",
                    "Positions initial margin sum",
                    "Positions PNL sum",
                ],
                "Value": [
                    "Binance",
                    "USDⓈ-M Futures",
                    symbol,
                    "{} - {} ({:.1f} days)".format(
                        date_from, date_to, result.get_interval_days()
                    ),
                    str(bot),
                    "{:.2f} $".format(result.get_average_tickers_price_change()),
                    "1 minute",
                    "{:,}".format(result.get_positions_count()),
                    "{:,.2f}".format(
                        result.get_positions_count() / result.get_interval_days()
                    ),
                    str(
                        timedelta(
                            milliseconds=result.get_positions_average_duration_millis()
                        )
                    ),
                    "{:,.2f}$ (abosolute)".format(
                        result.get_positions_average_price_margin()
                    ),
                    "1",
                    "{:,.2f} $".format(result.get_positions_average_initial_margin()),
                    "{:,.2f} $".format(result.get_positions_average_pnl()),
                    "{:,.2f} %".format(result.get_positions_average_roe() * 100.0),
                    "{:,.2f} $".format(result.get_positions_initial_margin_sum()),
                    "{:,.2f} $".format(result.get_positions_pnl_sum()),
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
        samples_count=100_000,
    )


def pnl_chart(result: BacktesterResult):
    st.subheader(f"PNL")
    if result.get_positions_count() > 0:
        pnl_chart_type = report_input.pnl_chart_type()

        match pnl_chart_type:
            case "PNL":
                report_chart.bars(
                    result.positions,
                    "entry_timestamp",
                    "pnl",
                    "PNL, $",
                    samples_count=100_000,
                )
            case _:
                report_chart.line(
                    result.positions,
                    "entry_timestamp",
                    "pnl",
                    "PNL sum (cumulative, aggregated), $",
                    samples_count=100_000,
                    is_cumulative=True,
                )

    else:
        st.text("There were NO positions! 😕")


def positions_table(positions: pd.DataFrame):
    st.subheader(f"Positions")
    st.dataframe(positions)
