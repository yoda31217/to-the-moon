from datetime import date
from datetime import timedelta
import pandas as pd

import streamlit as st
from report import report_input
import report.report_chart as report_chart
from backtester.backtester_result import BacktesterResult

from bot.bot import Bot
from streamlit.delta_generator import DeltaGenerator


def summary(
    symbol: str,
    date_from: date,
    date_to: date,
    bot: Bot,
    result: BacktesterResult,
    tab: DeltaGenerator,
):
    tab.table(
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


def tickers_chart(
    tickers: pd.DataFrame,
    tab: DeltaGenerator,
):
    report_chart.line(
        tab,
        tickers,
        "timestamp",
        "ask_price",
        "Ask Price, $",
        samples_count=100_000,
    )


def pnl_chart(
    result: BacktesterResult,
    tab: DeltaGenerator,
):
    if result.get_positions_count() > 0:
        pnl_chart_type = report_input.pnl_chart_type(tab)

        match pnl_chart_type:
            case "PNL sum":
                report_chart.bars(
                    tab,
                    result.positions,
                    result.positions_sort_timestamp_column,
                    "pnl",
                    "PNL sum, $",
                    samples_count=100_000,
                )
            case _:
                report_chart.line(
                    tab,
                    result.positions,
                    result.positions_sort_timestamp_column,
                    "pnl",
                    "cumulative PNL sum, $",
                    samples_count=100_000,
                    is_cumulative=True,
                )

    else:
        tab.text("There were NO positions! 😕")


def balances_chart(result: BacktesterResult, tab: DeltaGenerator):
    balance_chart_type = report_input.balance_chart_type(tab)
    
    match balance_chart_type:
        case "Margin Balance":
            report_chart.line(
                tab,
                result.balances,
                "timestamp",
                "margin_balance",
                "Margin Balance, $",
                samples_count=100_000,
            )
        case _:
            report_chart.line(
                tab,
                result.balances,
                "timestamp",
                "available_balance",
                "Available Balance, $",
                samples_count=100_000,
            )



def positions_table(positions: pd.DataFrame, tab: DeltaGenerator):
    tab.dataframe(positions)
