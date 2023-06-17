from datetime import date
import cProfile, pstats
from pstats import SortKey

from simulator.backtester.backtester import Backtester
from simulator.binance import binance_ticker_repository
from simulator.bot.bot_one_step_order import BotOneStepOrder

# Log:
# Optimisation 1:
# Baseline:
# ----
#          34854062 function calls (34854032 primitive calls) in 9.401 seconds
#
#    Ordered by: cumulative time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.008    0.008    9.401    9.401 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:29(test)
#      7201    0.005    0.000    6.793    0.001 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:60(_calculate_and_add_balance)
#     21603    0.282    0.000    6.782    0.000 {built-in method builtins.sum}
#      7201    0.005    0.000    5.941    0.001 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:76(_calculate_margin_balance)
#   5308698    2.742    0.000    4.971    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/order/order.py:54(get_pnl)
#   3278517    1.100    0.000    4.362    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:80(<genexpr>)
#      7200    0.159    0.000    2.134    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:100(_notify_orders)
#   1016585    0.325    0.000    1.976    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/order/order.py:74(notify)
#   1016585    0.397    0.000    1.542    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/order/order.py:107(_should_auto_close)
#   7347417    1.528    0.000    1.528    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/order/order.py:81(get_entry_price)
#   1023987    0.349    0.000    1.350    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:77(<genexpr>)
#   5311372    1.104    0.000    1.104    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/order/order.py:97(_get_exit_price)
# ====
# Final:
# ----
#          6490161 function calls (6490131 primitive calls) in 1.775 seconds
#
#    Ordered by: cumulative time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.014    0.014    1.775    1.775 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:29(test)
#     14636    0.106    0.000    1.009    0.000 {built-in method builtins.sum}
#   1023785    0.335    0.000    0.753    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:61(<genexpr>)
#      7200    0.145    0.000    0.617    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:103(_notify_orders)
#   1016585    0.189    0.000    0.472    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/order/order.py:98(notify)
#   1016585    0.358    0.000    0.358    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/order/order.py:68(calculate_possible_pnl)
#   1016585    0.282    0.000    0.282    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/order/order.py:105(_should_auto_close)
#   1023785    0.119    0.000    0.119    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:68(<genexpr>)
#      7200    0.007    0.000    0.110    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:94(_move_orders_to_closed)
#   1139923    0.065    0.000    0.065    0.000 /opt/homebrew/Cellar/python@3.11/3.11.3/Frameworks/Python.framework/Versions/3.11/lib/python3.11/typing.py:2233(cast)
#      7200    0.061    0.000    0.061    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:99(<listcomp>)
#      7200    0.040    0.000    0.040    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:96(<listcomp>)
#    119520    0.026    0.000    0.031    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/backtester/backtester.py:55(<genexpr>)
#      7200    0.004    0.000    0.016    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/bot/bot_one_step_order.py:36(process_ticker)
#      1337    0.002    0.000    0.008    0.000 /Users/nikita/Documents/projects/yoda31217/to-the-moon/simulator/order/order.py:31(__init__)
# ====

symbol = "ETHUSDT"
date_from = date.fromisoformat("2023-04-23")
date_to = date.fromisoformat("2023-04-27")
bid_ask_spread = 0.01

bot = BotOneStepOrder(
    dict(
        step_to_price_ratio=0.001,
        tp_to_entry_price_ratio=0.01,
        sl_to_entry_price_ratio=-0.1,
        inverted=False,
        order_quantity=1,
        order_leverage=1,
    )
)
tickers = binance_ticker_repository.load_tickers(
    symbol, date_from, date_to, bid_ask_spread
)

backtester = Backtester(tickers)

profiler = cProfile.Profile()
profiler.enable()

backtester.test(bot)

profiler.disable()
ps = pstats.Stats(profiler).sort_stats(SortKey.CUMULATIVE)
ps.print_stats()
