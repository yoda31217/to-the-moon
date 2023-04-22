import os
import streamlit as st
import pandas as pd

from binance.binance_k_line_loader import load_binance_k_lines
from binance.binance_tick_loader import load_binance_ticks

# from report.report import load_and_report_ticks
# import matplotlib.pyplot as plt
# import numpy as np


st.title('Simulation results')

st.text('Description1')

symbol_ask_bid_price_difference = 0.01

k_lines = load_binance_k_lines(f"./../ttm-data/ETHUSDT-1s-2023-03-01.csv")
ticks = load_binance_ticks(k_lines, symbol_ask_bid_price_difference)

st.dataframe(ticks)

    # draw_line_chart(ticks, 'timestamp', 'bid_price', 'Bid Price', 'Ticks')
    # display(ticks)

    # return ticks

# @st.cache_data
# def get_ticks_cached():
#     return load_and_report_ticks(
#     csv_files_pattern=f"./../ttm-data/ETHUSDT-1s-*.csv",
#     symbol_ask_bid_price_difference=0.01,
# )

# ticks = get_ticks_cached()

# ticks

# arr = np.random.normal(1, 1, size=100)
# fig, ax = plt.subplots()
# ax.hist(arr, bins=20)

# st.pyplot(fig)

# from trade.trade_simulator import TradeSimulator

# trade_simulator: TradeSimulator = TradeSimulator(ticks)

# from report.report import simulate_and_report
# from bot.bot_0_strategy import Bot0Strategy

# simulate_and_report([
#     # 'orders=30,049 interval_days=48.0 avg_tick_price_change=0.06 str=Bot0[0.10%, not_inverted]
#     # tx_avg_price_margin=1.99 tx_avg_prof=-0.04 tx_cum_prof=-1199.56'
#     Bot0Strategy(price_step_ratio=0.001, inverted=False),
#     Bot0Strategy(price_step_ratio=0.0025, inverted=False),
#     Bot0Strategy(price_step_ratio=0.005, inverted=False),
#     Bot0Strategy(price_step_ratio=0.0075, inverted=False),
#     Bot0Strategy(price_step_ratio=0.01, inverted=False),
#     Bot0Strategy(price_step_ratio=0.025, inverted=False),
#     Bot0Strategy(price_step_ratio=0.05, inverted=False),
#     Bot0Strategy(price_step_ratio=0.1, inverted=False),

#     Bot0Strategy(price_step_ratio=0.001, inverted=True),
#     Bot0Strategy(price_step_ratio=0.0025, inverted=True),
#     Bot0Strategy(price_step_ratio=0.005, inverted=True),
#     Bot0Strategy(price_step_ratio=0.0075, inverted=True),
#     Bot0Strategy(price_step_ratio=0.01, inverted=True),
#     Bot0Strategy(price_step_ratio=0.025, inverted=True),
#     Bot0Strategy(price_step_ratio=0.05, inverted=True),
#     Bot0Strategy(price_step_ratio=0.1, inverted=True),
# ], trade_simulator)
