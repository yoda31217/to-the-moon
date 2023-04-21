from IPython.core.display_functions import display

from binance.binance_k_line_loader import load_binance_k_lines
from binance.binance_tick_loader import load_binance_ticks
from chart.ttm_chart import draw_line_chart
from trade.trade_simulator import TradeSimulator
from trade.trade_simulator_strategy import TradeSimulatorStrategy


def load_and_report_ticks(csv_files_pattern: str, symbol_ask_bid_price_difference: float):
    k_lines = load_binance_k_lines(csv_files_pattern)
    ticks = load_binance_ticks(k_lines, symbol_ask_bid_price_difference)

    draw_line_chart(ticks, 'timestamp', 'bid_price', 'Bid Price', 'Ticks')
    display(ticks)

    return ticks


def simulate_and_report(strategies: [TradeSimulatorStrategy], trade_simulator: TradeSimulator):
    for strategy in strategies:
        result = trade_simulator.simulate(strategy)
        result_str = (f"orders={result.get_transactions_count() :,}"
                      f" avg_tick_price_change={trade_simulator.ticks_data_frame.ask_price.diff().abs().mean():.2f}"
                      f" str={strategy}"
                      f" tx_avg_price_margin={result.get_transactions_average_price_margin():.2f}"
                      f" tx_avg_prof={result.get_transactions_average_profit():.2f}"
                      f" tx_cum_prof={result.get_transactions_cumulative_profit():.2f}")
        draw_line_chart(result.transactions, 'open_timestamp', 'cumulative_profit', 'Cumulative Profit', result_str)
        display(result_str)
        # display(result)
