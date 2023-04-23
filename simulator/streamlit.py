import datetime
import sys
import streamlit as st
import pandas as pd
from binance.binance_tick_loader import load_binance_ticks
from bot.bot_0_strategy import Bot0Strategy
from chart.chart import draw_line_chart
from binance.binance_k_line_loader import _load_binance_k_lines_data_frame
from binance.binance_k_line_loader import BINANCE_SYMBOLS
from trade.trade_simulator import TradeSimulator
from datetime import date
from datetime import timedelta

# Options

st.sidebar.header("Опции")

st.sidebar.subheader("Стратегия: Bot0")

symbol = st.sidebar.selectbox(
    "Символ", options=BINANCE_SYMBOLS, index=BINANCE_SYMBOLS.index("ETHUSDT")
)

date_from_str = st.sidebar.date_input("Дата с", date.today() - timedelta(days=2))

date_to_str = st.sidebar.date_input("Дата по", date.today() - timedelta(days=2))

date_strs = (
    pd.date_range(date_from_str, date_to_str, freq="d").strftime("%Y-%m-%d").to_list()
)

symbol_ask_bid_price_difference = st.sidebar.number_input(
    "Разница цены купли-проажи", value=0.01
)

price_step_ratio = (
    st.sidebar.slider(
        "Шаг цены, %",
        min_value=0.1,
        max_value=10.0,
        value=0.1,
        step=0.1,
        help="На сколько должна изменить цена, что бы бот сделал действие",
    )
    / 100.0
)

inverted = st.sidebar.checkbox(
    "Инвертировать", value=False, help="Поменять местами покупку и продажу"
)

strategy = Bot0Strategy(price_step_ratio, inverted)


@st.cache_data
def load_binance_k_lines_with_cache(symbol: str, iso_date_str: str) -> pd.DataFrame:
    return _load_binance_k_lines_data_frame(
        f"https://data.binance.vision/data/spot/daily/klines/{symbol}/1s/{symbol}-1s-{iso_date_str}.zip"
    )


k_lines = pd.concat(
    [load_binance_k_lines_with_cache(symbol, date_str) for date_str in date_strs]
).sort_values(by=["open_timestamp_millis"])

ticks = load_binance_ticks(k_lines, symbol_ask_bid_price_difference)
result = TradeSimulator(ticks).simulate(strategy)

# Body

st.header(f"Симуляция торговли крипто бота")


st.text("Description1")

# 'orders=30,049 interval_days=48.0 avg_tick_price_change=0.06 str=Bot0[0.10%, not_inverted]
# tx_avg_price_margin=1.99 tx_avg_prof=-0.04 tx_cum_prof=-1199.56'

# 03/01 - -16.09 - 431 - 0.1%

st.subheader(f"Сводка")
st.table(
    pd.DataFrame(
        {
            "Показатель": [
                "Символ",
                "Данные",
                "Название стратегии",
                "Инвертирован",
                "Среднее изменение цены за тик",
                "Интервал симуляции",
                "Количество транзакций",
                "Количество транзакций в день",
                "Средняя ценовая маржа транзакции",
                "Средняя прибыль транзакции",
                "Итоговая прибыль",
            ],
            "Значение": [
                symbol,
                "Binance",
                strategy,
                "Да" if inverted else "Нет",
                "{:.2f}".format(result.get_average_ticks_price_change()),
                "c {} по {} ({:.1f} дней)".format(date_from_str, date_to_str, result.get_interval_days()),
                result.get_transactions_count(),
                "{:.2f}".format(result.get_transactions_count() / result.get_interval_days()),
                "{:.2f}".format(result.get_transactions_average_price_margin()),
                "{:.2f}".format(result.get_transactions_average_profit()),
                "{:.2f}".format(result.get_transactions_cumulative_profit()),
            ],
        }
    )
)


st.subheader(f"Цена покупки")
draw_line_chart(
    ticks,
    "timestamp",
    "ask_price",
    "Цена покупки, $",
    samples_count=1000,
)

st.subheader(f"Итоговая прибыль")
if result.get_transactions_count() > 0:
    draw_line_chart(
        result.transactions,
        "open_timestamp",
        "cumulative_profit",
        "Итоговая прибыль, $",
        samples_count=1000000,
    )
else:
    st.text("Нет транзакций! 😕")
