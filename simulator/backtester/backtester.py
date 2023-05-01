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

        balances = pd.DataFrame(
            {
                "timestamp": [],
                "margin_balance": [],
            }
        )

        for new_ticker in self.tickers:
            self._notify_orders(new_ticker, orders)
            self._move_orders_to_closed(orders, closed_orders)

            bot.process_ticker(new_ticker, orders, closed_orders)

            self._calculate_and_add_balance(orders, closed_orders, balances, new_ticker)

        self._close_orders(orders)
        self._move_orders_to_closed(orders, closed_orders)

        return BacktesterResult(
            closed_orders,
            self.tickers_data_frame,
            positions_sort_timestamp_column,
            balances,
        )

    def _calculate_and_add_balance(self, orders, closed_orders, balances, new_ticker):
        data_frame_add_row(
            balances,
            [
                new_ticker.timestamp,
                self._calculate_margin_balance(orders, closed_orders, new_ticker),
            ],
        )

    def _calculate_margin_balance(self, orders, closed_orders, new_ticker):
        orders_margin_balance = sum(
            cast(float, order.get_pnl(new_ticker)) for order in orders
        )
        closed_orders_margin_balance = sum(
            cast(float, order.get_pnl(new_ticker)) for order in closed_orders
        )
        return orders_margin_balance + closed_orders_margin_balance

    def _close_orders(self, orders: list[Order]):
        order: Order
        for order in orders:
            if order.is_open():
                order.close(self.tickers[-1])

    @staticmethod
    def _move_orders_to_closed(orders: list[Order], closed_orders: list[Order]):
        new_closed_orders = [order for order in orders if not order.is_open()]
        closed_orders.extend(new_closed_orders)

        open_orders = [order for order in orders if order.is_open()]
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
