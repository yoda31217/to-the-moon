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

    def __init__(
        self,
        open_tick: MarketTicker,
        side: OrderSide,
        tp_to_entry_price_ratio: float,
        sl_to_entry_price_ratio: float,
    ):
        self.id = uuid.uuid4()
        self.side = side
        self.entry_ticker = open_tick
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

    def get_initial_margin(self):
        return self.get_entry_price()

    def is_open(self) -> bool:
        return self.exit_ticker == None

    def get_pnl(self, new_ticker: MarketTicker | None = None) -> float | None:
        exit_price = (
            self._get_exit_price(self.exit_ticker)
            if self.exit_ticker != None
            else self._get_exit_price(new_ticker)
        )

        if exit_price == None:
            return None

        entry_price = self.get_entry_price()
        return (
            exit_price - entry_price
            if self.side == OrderSide.BUY
            else entry_price - exit_price
        )

    def close(self, ticker: MarketTicker):
        self.exit_ticker = ticker

    def notify(self, new_ticker: MarketTicker):
        if not self.is_open():
            return

        if self._should_auto_close(new_ticker):
            self.close(new_ticker)

    def get_entry_price(self) -> float:
        return (
            self.entry_ticker.bid_price
            if self.side == OrderSide.SELL
            else self.entry_ticker.ask_price
        )

    def get_exit_price(self) -> float | None:
        return self._get_exit_price(self.exit_ticker)

    def get_roe(self) -> float | None:
        if self.get_pnl() == None:
            return None

        return cast(float, self.get_pnl()) / self.get_initial_margin()

    def _get_exit_price(self, possible_exit_ticker: MarketTicker | None):
        if possible_exit_ticker == None:
            return None

        return (
            possible_exit_ticker.ask_price
            if self.side == OrderSide.SELL
            else possible_exit_ticker.bid_price
        )

    def _should_auto_close(self, possible_exit_ticker: MarketTicker):
        pnl = self.get_pnl(possible_exit_ticker)
        assert pnl is not None

        pnl_to_entry_price_ratio = pnl / self.get_entry_price()

        return (
            pnl_to_entry_price_ratio >= self.tp_to_entry_price_ratio
            or pnl_to_entry_price_ratio <= self.sl_to_entry_price_ratio
        )
