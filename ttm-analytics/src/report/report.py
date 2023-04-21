from IPython.core.display_functions import display

from binance.binance_k_line_loader import load_binance_k_lines
from binance.binance_tick_loader import load_binance_ticks
from chart.ttm_chart import draw_line_chart


def load_and_report_ticks(csv_files_pattern: str, symbol_ask_bid_price_difference: float):
    k_lines = load_binance_k_lines(csv_files_pattern)
    ticks = load_binance_ticks(k_lines, symbol_ask_bid_price_difference)

    draw_line_chart(ticks, 'timestamp', 'bid_price', 'Bid Price', 'Ticks')
    display(ticks)

    return ticks
