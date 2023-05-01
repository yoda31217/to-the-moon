from typing import cast
import uuid

from order.order_side import OrderSide
from market.market_ticker import MarketTicker


# According to:
# https://www.binance.com/en/futures/ETHUSDT/calculator
# https://binance-docs.github.io/apidocs/futures/en/#new-order-trade
# https://www.binance.com/en/support/faq/how-to-calculate-profit-and-loss-for-futures-contracts-3a55a23768cb416fb404f06ffedde4b2
class Order:
    id: uuid.UUID
    side: OrderSide
    entry_ticker: MarketTicker
    exit_ticker: MarketTicker | None
    # TODO: migrate to TP/SL prices.
    # Problem here, that our TP  = real_TP - entry_price
    tp_to_entry_price_ratio: float
    sl_to_entry_price_ratio: float

    entry_price: float
    exit_price: float | None
    initial_margin: float
    pnl: float | None
    tp: float
    sl: float
    is_open: bool
    roe: float | None

    def __init__(
        self,
        entry_ticker: MarketTicker,
        side: OrderSide,
        tp_to_entry_price_ratio: float,
        sl_to_entry_price_ratio: float,
    ):
        self.id = uuid.uuid4()
        self.side = side
        self.entry_ticker = entry_ticker
        self.exit_ticker = None
        self.tp_to_entry_price_ratio = tp_to_entry_price_ratio
        self.sl_to_entry_price_ratio = sl_to_entry_price_ratio

        if self.sl_to_entry_price_ratio > 0:
            raise ValueError(
                f"Order SL to entry price ratio should be <= 0,"
                + f" but was: ${self.sl_to_entry_price_ratio}."
            )

        if self.tp_to_entry_price_ratio < 0:
            raise ValueError(
                f"Order TP to entry price ratio should be >= 0,"
                + f" but was: ${self.tp_to_entry_price_ratio}."
            )

        self.entry_price = (
            entry_ticker.bid_price if side == OrderSide.SELL else entry_ticker.ask_price
        )
        self.exit_price = None
        self.initial_margin = self.entry_price
        self.pnl = None
        self.tp = tp_to_entry_price_ratio * self.entry_price
        self.sl = sl_to_entry_price_ratio * self.entry_price
        self.is_open = True
        self.roe = None

    def calculate_possible_pnl(self, possible_exit_ticker: MarketTicker) -> float:
        if self.pnl != None:
            return self.pnl
        else:
            possible_exit_price = (
                possible_exit_ticker.ask_price
                if self.side == OrderSide.SELL
                else possible_exit_ticker.bid_price
            )
            return (
                possible_exit_price - self.entry_price
                if self.side == OrderSide.BUY
                else self.entry_price - possible_exit_price
            )

    def close(self, ticker: MarketTicker):
        self.exit_ticker = ticker
        exit_price = (
            ticker.ask_price if self.side == OrderSide.SELL else ticker.bid_price
        )
        self.exit_price = exit_price
        pnl = (
            exit_price - self.entry_price
            if self.side == OrderSide.BUY
            else self.entry_price - exit_price
        )
        self.pnl = pnl
        self.roe = pnl / self.initial_margin
        self.is_open = False

    def notify(self, new_ticker: MarketTicker):
        if not self.is_open:
            return

        if self._should_auto_close(new_ticker):
            self.close(new_ticker)

    def _should_auto_close(self, possible_exit_ticker: MarketTicker):
        possible_pnl = (
            possible_exit_ticker.bid_price - self.entry_price
            if self.side == OrderSide.BUY
            else self.entry_price - possible_exit_ticker.ask_price
        )

        return possible_pnl >= self.tp or possible_pnl <= self.sl
