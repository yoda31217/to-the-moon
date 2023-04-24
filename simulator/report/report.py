from datetime import date, timedelta
from typing import cast
import pandas as pd
import streamlit as st
from binance.binance_k_line_loader import BINANCE_SYMBOLS
from chart.chart import draw_line_chart
from trade.trade_simulator_result import TradeSimulatorResult

from trade.trade_simulator_strategy import TradeSimulatorStrategy


def text_description():
    with st.expander("Описание", expanded=False):
        st.write(
            """
                Привет!
                
                Проект открытый. Вот
                исходники проекта на [GitHub](https://github.com/yoda31217/to-the-moon)
                и пример 
                [Бота](https://github.com/yoda31217/to-the-moon/blob/main/simulator/bot/bot_0_strategy.py).
            """
        )


def input_symbol_widget():
    return cast(
        str,
        st.sidebar.selectbox(
            "Символ", options=BINANCE_SYMBOLS, index=BINANCE_SYMBOLS.index("ETHUSDT")
        ),
    )


def input_date_from_widget():
    return cast(date, st.sidebar.date_input("Дата с", date.today() - timedelta(days=2)))


def input_date_to_widget():
    return cast(
        date, st.sidebar.date_input("Дата по", date.today() - timedelta(days=2))
    )


def input_price_step_ratio_widget():
    return (
        st.sidebar.slider(
            "Шаг цены, %",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="На сколько должна измениться цена, что бы бот сделал действие",
        )
        / 100.0
    )


def input_inverted_widget():
    return st.sidebar.checkbox(
        "Инвертировать",
        value=False,
        help="Поменять местами покупку и продажу в алгоритме",
    )


def input_symbol_ask_bid_price_difference_widget():
    return st.sidebar.number_input("Разница цены купли-проажи", value=0.01)


def report_summary(
    symbol: str,
    date_from: date,
    date_to: date,
    strategy: TradeSimulatorStrategy,
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
                    "Bot",
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
                    strategy,
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


def report_ticks_chart(ticks: pd.DataFrame):
    st.subheader(f"Цена покупки")
    draw_line_chart(
        ticks,
        "timestamp",
        "ask_price",
        "Цена покупки, $",
        samples_count=1_000,
    )


def report_profit_chart(result: TradeSimulatorResult):
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
