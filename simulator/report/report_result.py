from datetime import date
import pandas as pd

import streamlit as st
from chart.chart import draw_line_chart
from trade.trade_simulator_result import TradeSimulatorResult

from bot.bot import Bot


def summary(
    symbol: str,
    date_from: date,
    date_to: date,
    bot: Bot,
    result: TradeSimulatorResult,
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
                    bot,
                    "{:.2f}".format(result.get_average_ticks_price_change()),
                    "{:,}".format(result.get_transactions_count()),
                    "{:,.2f}".format(
                        result.get_transactions_count() / result.get_interval_days()
                    ),
                    "{:,.2f} (по модулю)".format(
                        result.get_transactions_average_price_margin()
                    ),
                    "1",
                    "{:,.2f}".format(result.get_transactions_average_profit()),
                    "{:,.2f}".format(result.get_transactions_average_return()),
                    "{:,.2f}".format(result.get_transactions_cumulative_profit()),
                    "{:,.2f}".format(result.get_transactions_cumulative_return()),
                ],
            }
        )
    )


def ticks_chart(ticks: pd.DataFrame):
    st.subheader(f"Цена покупки")
    draw_line_chart(
        ticks,
        "timestamp",
        "ask_price",
        "Цена покупки, $",
        samples_count=1_000,
    )


def profit_chart(result: TradeSimulatorResult):
    st.subheader(f"Итоговая прибыль")
    if result.get_transactions_count() > 0:
        draw_line_chart(
            result.transactions,
            "open_timestamp",
            "cumulative_profit",
            "Итоговая прибыль, $",
            samples_count=10_000,
        )
    else:
        st.text("Нет транзакций! 😕")
