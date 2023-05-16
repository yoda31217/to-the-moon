from typing import cast
import pandas as pd
from bot.bot import Bot

from order.order import Order
from market.market_ticker import MarketTicker, MarketTikersDataFrame
from utils.series import TypedSeries


class BacktesterResultPositionsDataFrame(pd.DataFrame):
    entry_timestamp: TypedSeries[int]
    exit_timestamp: TypedSeries[int]
    durarion_millis: TypedSeries[int]
    side: TypedSeries[str]
    entry_price: TypedSeries[float]
    exit_price: TypedSeries[float]
    price_margin: TypedSeries[float]
    quantity: TypedSeries[float]
    initial_margin: TypedSeries[float]
    pnl: TypedSeries[float]
    roe: TypedSeries[float]


class BacktesterResult:
    bot: Bot
    positions: BacktesterResultPositionsDataFrame
    tickers: MarketTikersDataFrame
    balances: pd.DataFrame

    def __init__(
        self,
        bot: Bot,
        closed_orders: list[Order],
        tickers: MarketTikersDataFrame,
        balances: pd.DataFrame,
    ) -> None:
        super().__init__()
        self.bot = bot
        self.tickers = tickers
        self.positions = self._to_positions(closed_orders)
        self.balances = balances

    def _to_positions(
        self, closed_orders: list[Order]
    ) -> BacktesterResultPositionsDataFrame:
        data_frame = pd.DataFrame(
            {
                "entry_timestamp": list(
                    (
                        closed_order.entry_ticker.timestamp
                        for closed_order in closed_orders
                    )
                ),
                "exit_timestamp": list(
                    (
                        cast(MarketTicker, closed_order.exit_ticker).timestamp
                        for closed_order in closed_orders
                    )
                ),
                "durarion_millis": list(
                    (
                        cast(MarketTicker, closed_order.exit_ticker).timestamp
                        - closed_order.entry_ticker.timestamp
                        for closed_order in closed_orders
                    )
                ),
                "side": list(
                    (closed_order.side.name for closed_order in closed_orders)
                ),
                "entry_price": list(
                    (closed_order.entry_price for closed_order in closed_orders)
                ),
                "exit_price": list(
                    (closed_order.exit_price for closed_order in closed_orders)
                ),
                "price_margin": list(
                    (
                        abs(
                            cast(float, closed_order.exit_price)
                            - closed_order.entry_price
                        )
                        for closed_order in closed_orders
                    )
                ),
                "quantity": list(
                    (closed_order.quantity for closed_order in closed_orders)
                ),
                "initial_margin": list(
                    (closed_order.initial_margin for closed_order in closed_orders)
                ),
                "pnl": list((closed_order.pnl for closed_order in closed_orders)),
                "roe": list((closed_order.roe for closed_order in closed_orders)),
            }
        )
        return cast(BacktesterResultPositionsDataFrame, data_frame)

    def get_positions_count(self):
        return len(self.positions.index)

    def get_positions_average_price_margin(self) -> float:
        return self.positions.price_margin.mean()

    def get_positions_average_pnl(self):
        return self.positions.pnl.mean()

    def get_positions_average_duration_millis(self):
        return self.positions.durarion_millis.mean()

    def get_positions_average_initial_margin(self):
        return self.positions.initial_margin.mean()

    def get_positions_average_quantity(self):
        return self.positions.quantity.mean()

    def get_positions_initial_margin_sum(self):
        return self.positions.initial_margin.sum()

    def get_positions_average_roe(self):
        return self.positions.roe.mean()

    def get_positions_pnl_sum(self):
        return self.positions.pnl.sum() if self.get_positions_count() > 0 else 0

    def get_average_tickers_price_change(self):
        return self.tickers.ask_price.diff().abs().mean()

    def get_interval_days(self) -> float:
        min_timestamp = self.tickers.timestamp.min()
        max_timestamp = self.tickers.timestamp.max()
        return (max_timestamp - min_timestamp) / (1.0 * 24 * 60 * 60 * 1000)
