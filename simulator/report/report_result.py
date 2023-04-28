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
    # values to check (like a test)
    # 'orders=30,049 interval_days=48.0 avg_tick_price_change=0.06 str=Bot0[0.10%, not_inverted]
    # tx_avg_price_margin=1.99 tx_avg_prof=-0.04 tx_cum_prof=-1199.56'

    st.subheader(f"Сводка")
    st.table(
        pd.DataFrame(
            {
                "Показатель": [
                    "Биржа",
                    "Символ",
                    "Интервал симуляции",
                    "Бот",
                    "Среднее изменение цены за тик",
                    "Количество транзакций",
                    "Количество транзакций в день",
                    "Средняя ценовая маржа транзакции",
                    "Сколько монет в транзакции",
                    "Средняя прибыль транзакции",
                    "Средний оборот транзакции",
                    "Итоговая прибыль",
                    "Итоговый оборот",
                ],
                "Значение": [
                    "Binance",
                    symbol,
                    "c {} по {} ({:.1f} дней)".format(
                        date_from, date_to, result.get_interval_days()
                    ),
                    str(bot),
                    "{:.2f}".format(result.get_average_tickers_price_change()),
                    "{:,}".format(result.get_positions_count()),
                    "{:,.2f}".format(
                        result.get_positions_count() / result.get_interval_days()
                    ),
                    "{:,.2f} (по модулю)".format(
                        result.get_positions_average_price_margin()
                    ),
                    "1",
                    "{:,.2f}".format(result.get_positions_average_pnl()),
                    "{:,.2f}".format(result.get_transactions_average_return()),
                    "{:,.2f}".format(result.get_positions_balance()),
                    "{:,.2f}".format(result.get_transactions_cumulative_return()),
                ],
            }
        )
    )


def ticks_chart(ticks: pd.DataFrame):
    st.subheader(f"Цена покупки")
    report_chart.line(
        ticks,
        "timestamp",
        "ask_price",
        "Цена покупки, $",
        samples_count=1_000,
    )


def profit_chart(result: BacktesterResult):
    st.subheader(f"Итоговая прибыль")
    if result.get_positions_count() > 0:
        report_chart.line(
            result.positions,
            "open_timestamp",
            "cumulative_profit",
            "Итоговая прибыль, $",
            samples_count=10_000,
        )
    else:
        st.text("Нет транзакций! 😕")
