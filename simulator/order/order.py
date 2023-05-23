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
    # TODO: migrate to TP/SL prices.
    # Problem here, that our TP  = real_TP - entry_price
    tp_to_entry_price_ratio: float
    sl_to_entry_price_ratio: float
    quantity: float
    leverage: float

    entry_price: float
    exit_price: float | None
    initial_margin: float
    pnl: float | None
    _tp_price: float
    _sl_price: float
    is_open: bool
    roe: float | None

    def __init__(
        self,
        entry_ticker: MarketTicker,
        side: OrderSide,
        tp_to_entry_price_ratio: float,
        sl_to_entry_price_ratio: float,
        quantity: float = 1.0,
        leverage: float = 1.0,
    ):
        self.id = uuid.uuid4()
        self.side = side
        self.entry_ticker = entry_ticker
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
        self.initial_margin = self.entry_price * quantity / leverage
        self.pnl = None
        self._tp_price = (
            (1 + tp_to_entry_price_ratio) * self.entry_price * quantity
            if side == OrderSide.BUY
            else (1 - tp_to_entry_price_ratio) * self.entry_price * quantity
        )
        self._sl_price = (
            (1 - tp_to_entry_price_ratio) * self.entry_price * quantity
            if side == OrderSide.BUY
            else (1 + tp_to_entry_price_ratio) * self.entry_price * quantity
        )
        self.is_open = True
        self.roe = None
        self.quantity = quantity
        self.leverage = leverage

    def calculate_possible_pnl(
        self, possible_exit_ticker_or_price: MarketTicker | float
    ) -> float:
        if self.pnl != None:
            return self.pnl

        possible_exit_price = (
            self._get_possible_exit_price(possible_exit_ticker_or_price)
            if isinstance(possible_exit_ticker_or_price, MarketTicker)
            else possible_exit_ticker_or_price
        )

        return (
            possible_exit_price - self.entry_price
            if self.side == OrderSide.BUY
            else self.entry_price - possible_exit_price
        ) * self.quantity

    def close(self, ticker: MarketTicker):
        if not self.is_open:
            raise Exception(f"Failed to close already closed order.")

        self.exit_price = self._get_possible_exit_price(ticker)
        self.pnl = self.calculate_possible_pnl(self.exit_price)
        self.roe = self.pnl / self.initial_margin
        self.is_open = False

    def _get_possible_exit_price(self, possible_exit_ticker: MarketTicker):
        return (
            possible_exit_ticker.ask_price
            if self.side == OrderSide.SELL
            else possible_exit_ticker.bid_price
        )

    def auto_close_if_needed(self, new_ticker: MarketTicker):
        if not self.is_open:
            return

        if self._should_auto_close(new_ticker):
            self.close(new_ticker)

    def _should_auto_close(self, possible_exit_ticker: MarketTicker):
        possible_exit_price = self._get_possible_exit_price(possible_exit_ticker)
        return (
            possible_exit_price >= self._tp_price
            or possible_exit_price <= self._sl_price
        )
