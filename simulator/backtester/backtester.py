import timeit
from typing import NamedTuple, cast
import pandas as pd
from backtester.backtester_result import BacktesterResult

from order.order import Order
from bot.bot import Bot
from market.market_ticker import MarketTicker
from utils.data_frames import data_frame_add_row

TickersDataFrameRowTuple = NamedTuple(
    "Employee", timestamp=int, bid_price=float, ask_price=float
)


class Backtester:
    tickers: list[MarketTicker]
    tickers_data_frame: pd.DataFrame

    def __init__(self, tickers_data_frame: pd.DataFrame) -> None:
        self.tickers = list(
            (
                self._to_ticker(ticker_row)
                for ticker_row in tickers_data_frame.itertuples()
            )
        )
        self.tickers_data_frame = tickers_data_frame

    def test(self, bot: Bot, positions_sort_timestamp_column: str) -> BacktesterResult:
        orders: list[Order] = []
        closed_orders: list[Order] = []

        balances = [[0, 0, 0]] * (len(self.tickers))

        closed_orders_count_cache = 0.0
        closed_orders_margin_balance_cache = 0.0

        for new_ticker_index, new_ticker in enumerate(self.tickers):
            self._notify_orders(new_ticker, orders)

            bot.process_ticker(new_ticker, orders, closed_orders)

            if new_ticker_index == len(self.tickers) - 1:
                self._close_orders(orders)

            self._move_orders_to_closed(orders, closed_orders)

            # calculate_and_add_balance.START (performance optimisation; inlined)

            closed_orders_margin_balance: float

            if len(closed_orders) == closed_orders_count_cache:
                closed_orders_margin_balance = closed_orders_margin_balance_cache
            else:
                closed_orders_margin_balance = sum(
                    cast(float, order.get_pnl()) for order in closed_orders
                )
                closed_orders_margin_balance_cache = closed_orders_margin_balance
                closed_orders_count_cache = len(closed_orders)

            orders_margin_balance = sum(
                cast(float, order.get_pnl(new_ticker)) for order in orders
            )

            margin_balance = orders_margin_balance + closed_orders_margin_balance

            available_balance = margin_balance - sum(
                order.initial_margin for order in orders if order.is_open
            )

            balances[new_ticker_index] = [
                new_ticker.timestamp,
                margin_balance,
                available_balance,
            ]
            # calculate_and_add_balance.FINISH

        return BacktesterResult(
            closed_orders,
            self.tickers_data_frame,
            positions_sort_timestamp_column,
            pd.DataFrame(
                balances, columns=["timestamp", "margin_balance", "available_balance"]
            ),
        )

    def _close_orders(self, orders: list[Order]):
        order: Order
        for order in orders:
            if order.is_open:
                order.close(self.tickers[-1])

    @staticmethod
    def _move_orders_to_closed(orders: list[Order], closed_orders: list[Order]):
        new_closed_orders = [order for order in orders if not order.is_open]
        closed_orders.extend(new_closed_orders)

        open_orders = [order for order in orders if order.is_open]
        orders.clear()
        orders.extend(open_orders)

    @staticmethod
    def _notify_orders(ticker, orders: list[Order]):
        order: Order
        for order in orders:
            order.notify(ticker)

    @staticmethod
    def _to_ticker(ticker_row: TickersDataFrameRowTuple):
        return MarketTicker(
            ticker_row.timestamp, ticker_row.bid_price, ticker_row.ask_price
        )
