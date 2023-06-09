from datetime import date
from datetime import timedelta
import pandas as pd
from bot.bot import Bot
from streamlit.delta_generator import DeltaGenerator


from simulator.report import report_input
import simulator.report.report_chart as report_chart
from simulator.backtester.backtester_result import BacktesterResult
from simulator.utils import data_frames, dicts


def summary(
    symbol: str,
    date_from: date,
    date_to: date,
    result: BacktesterResult,
    tab: DeltaGenerator,
):
    tab.table(  # pyright: ignore [reportUnknownMemberType]
        pd.DataFrame(
            {
                "Property": [
                    "Exchange",
                    "Market",
                    "Symbol",
                    "Test interval",
                    "Tickers price change mean, median",
                    "Tickers average interval",
                    "Positions count",
                    "Positions count / day",
                    "Positions duration mean, median",
                    "Positions quantity mean, median",
                    "Positions initial margin mean, median",
                    "Positions PNL mean, median",
                    "Positions ROE mean, median",
                    "Positions initial margin sum",
                    "Positions PNL sum",
                ],
                "Value": [
                    "Binance",
                    "USDⓈ-M Futures",
                    symbol,
                    "{} - {} ({:.1f})".format(
                        date_from, date_to, result.get_interval_days()
                    ),
                    "{:.2f}, {:.2f}".format(
                        result.get_mean_tickers_price_change(),
                        result.get_median_tickers_price_change(),
                    ),
                    "1",
                    "{:,}".format(result.get_positions_count()),
                    "{:,.2f}".format(
                        result.get_positions_count() / result.get_interval_days()
                    ),
                    str(
                        timedelta(
                            milliseconds=result.get_positions_mean_duration_millis()
                        )
                    )
                    + ", "
                    + str(
                        timedelta(
                            milliseconds=result.get_positions_median_duration_millis()
                        )
                    ),
                    "{:,.2f}, {:,.2f}".format(
                        result.get_positions_mean_quantity(),
                        result.get_positions_median_quantity(),
                    ),
                    "{:,.2f}, {:,.2f}".format(
                        result.get_positions_mean_initial_margin(),
                        result.get_positions_median_initial_margin(),
                    ),
                    "{:,.2f}, {:,.2f}".format(
                        result.get_positions_mean_pnl(),
                        result.get_positions_median_pnl(),
                    ),
                    "{:,.2f}, {:,.2f}".format(
                        result.get_positions_mean_roe() * 100.0,
                        result.get_positions_median_roe() * 100.0,
                    ),
                    "{:,.2f}".format(result.get_positions_initial_margin_sum()),
                    "{:,.2f}".format(result.get_positions_pnl_sum()),
                ],
                "Units": [
                    "-",
                    "-",
                    "-",
                    "Days",
                    "$",
                    "Minute",
                    "Count",
                    "Count / day",
                    "Duration",
                    "Quantity",
                    "$",
                    "$",
                    "%",
                    "$",
                    "$",
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
        positions_sort_timestamp_column = report_input.positions_sort_timestamp_column(
            "pnl_chart", tab
        )
        sorted_positions = data_frames.sort_by(
            result.positions, positions_sort_timestamp_column
        )

        match pnl_chart_type:
            case "PNL sum":
                report_chart.bars(
                    tab,
                    sorted_positions,
                    positions_sort_timestamp_column,
                    "pnl",
                    "PNL sum, $",
                    samples_count=100_000,
                )
            case _:
                report_chart.line(
                    tab,
                    sorted_positions,
                    positions_sort_timestamp_column,
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
    positions_sort_timestamp_column = report_input.positions_sort_timestamp_column(
        "positions_table", tab
    )
    tab.dataframe(  # pyright: ignore [reportUnknownMemberType]
        data_frames.sort_by(positions, positions_sort_timestamp_column)
    )


def bot_summary(bot: Bot, tab: DeltaGenerator):
    tab.subheader("Name")
    tab.text(bot.get_name())
    tab.subheader("Config")
    tab.code(dicts.to_json(bot.config))


def positions_histogram(result: BacktesterResult, tab: DeltaGenerator):
    positions_attribute = report_input.positions_histogram_attribute(tab)
    report_chart.histogram(
        tab, result.positions, positions_attribute, positions_attribute, "Position(s)"
    )
