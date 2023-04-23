import streamlit as st
from binance.binance_k_line_loader import load_binance_k_lines
from binance.binance_tick_loader import load_binance_ticks
from bot.bot_0_strategy import Bot0Strategy
from chart.chart import draw_line_chart
from trade.trade_simulator import TradeSimulator

st.sidebar.header("Опции")

st.sidebar.subheader("Стратегия: Bot0")

symbol = "ETHUSDT"
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


st.title("Результаты симуляции")

st.text("Description1")

k_lines = load_binance_k_lines(f"./ttm-data/{symbol}-1s-2023-03-01.csv")

ticks = load_binance_ticks(k_lines, symbol_ask_bid_price_difference)

# st.dataframe(ticks)

st.subheader(f"Цена покупки, symbol={symbol}")

draw_line_chart(ticks, "timestamp", "bid_price", "Цена покупки ($)")

trade_simulator: TradeSimulator = TradeSimulator(ticks)

st.subheader(f"Profit")

#     # 'orders=30,049 interval_days=48.0 avg_tick_price_change=0.06 str=Bot0[0.10%, not_inverted]
#     # tx_avg_price_margin=1.99 tx_avg_prof=-0.04 tx_cum_prof=-1199.56'

result = trade_simulator.simulate(Bot0Strategy(price_step_ratio, inverted))

if result.get_transactions_count() > 0:
    draw_line_chart(
        result.transactions,
        "open_timestamp",
        "cumulative_profit",
        "Итоговая прибыль ($)",
    )
else:
    st.caption("No Transactions! 😕")

    # result_str = (f"orders={result.get_transactions_count() :,}"
    #               f" interval_days={result.get_interval_days():.1f}"
    #               f" avg_tick_price_change={result.get_average_ticks_price_change():.2f}"
    #               f" str={strategy}"
    #               f" tx_avg_price_margin={result.get_transactions_average_price_margin():.2f}"
    #               f" tx_avg_prof={result.get_transactions_average_profit():.2f}"
    #               f" tx_cum_prof={result.get_transactions_cumulative_profit():.2f}")

    # display(result_str)
    # display(result)
