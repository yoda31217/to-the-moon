from datetime import date

from backtester.backtester import Backtester
from binance import binance_ticker_repository
from bot.bot_one_step_order import BotOneStepOrder
import cProfile, pstats, io
from pstats import SortKey


symbol = "ETHUSDT"
date_from = date.fromisoformat("2023-04-23")
date_to = date.fromisoformat("2023-04-29")
bid_ask_spread = 0.01
step_to_price_ratio = 0.01
tp_to_entry_price_ratio = 0.01
sl_to_entry_price_ratio = -0.01
inverted = False
positions_sort_timestamp_column = "entry_timestamp"

bot = BotOneStepOrder(
    step_to_price_ratio, tp_to_entry_price_ratio, sl_to_entry_price_ratio, inverted
)
tickers = binance_ticker_repository.load_tickers(
    symbol, date_from, date_to, bid_ask_spread
)

backtester = Backtester(tickers)

profiler = cProfile.Profile()
profiler.enable()

backtester.test(bot, positions_sort_timestamp_column)

profiler.disable()
s = io.StringIO()
ps = pstats.Stats(profiler, stream=s).sort_stats(SortKey.CUMULATIVE)
ps.print_stats()
print(s.getvalue())
