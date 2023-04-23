import streamlit as st
import pandas as pd
from binance.binance_tick_loader import load_binance_ticks
from bot.bot_0_strategy import Bot0Strategy
from chart.chart import draw_line_chart
from binance.binance_k_line_loader import _load_binance_k_lines_data_frame
from trade.trade_simulator import TradeSimulator

# Options

st.sidebar.header("Опции")

st.sidebar.subheader("Стратегия: Bot0")

symbol = "ETHUSDT"

iso_date_str = "2023-03-01"

symbol_ask_bid_price_difference = 0.01

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

# Body

st.text("Description1")


@st.cache_data
def load_binance_k_lines_with_cache(symbol: str, iso_date_str: str) -> pd.DataFrame:
    return _load_binance_k_lines_data_frame(
        f"https://data.binance.vision/data/spot/daily/klines/{symbol}/1s/{symbol}-1s-{iso_date_str}.zip"
    )


st.subheader(f"Цена покупки, символ={symbol}")
k_lines = load_binance_k_lines_with_cache(symbol, iso_date_str)
ticks = load_binance_ticks(k_lines, symbol_ask_bid_price_difference)
draw_line_chart(ticks, "timestamp", "bid_price", "Цена покупки, $")

trade_simulator: TradeSimulator = TradeSimulator(ticks)
result = trade_simulator.simulate(strategy)

st.header("Результаты")

st.subheader(f"Итоговая прибыль")
if result.get_transactions_count() > 0:
    draw_line_chart(
        result.transactions,
        "open_timestamp",
        "cumulative_profit",
        "Итоговая прибыль, $",
        samples_count=1_000_000,
    )
else:
    st.caption("No Transactions! 😕")


# 'orders=30,049 interval_days=48.0 avg_tick_price_change=0.06 str=Bot0[0.10%, not_inverted]
# tx_avg_price_margin=1.99 tx_avg_prof=-0.04 tx_cum_prof=-1199.56'

st.subheader(f"Сводка")
st.table(
    pd.DataFrame(
        {
            "Показатель": [
                "Символ",
                "Количество транзакций",
                "Интервал симуляции, день",
                "Среднее изменение цены за тик",
                "Название стратегии",
                "Средняя ценовая маржа транзакции",
                "Средняя прибыль транзакции",
                "Итоговая прибыль",
            ],
            "Значение": [
                symbol,
                result.get_transactions_count(),
                "{:.1f}".format(result.get_interval_days()),
                "{:.2f}".format(result.get_average_ticks_price_change()),
                strategy,
                "{:.2f}".format(result.get_transactions_average_price_margin()),
                "{:.2f}".format(result.get_transactions_average_profit()),
                "{:.2f}".format(result.get_transactions_cumulative_profit()),
            ],
        }
    )
)
