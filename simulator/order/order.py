import uuid

from order.order_side import OrderSide
from market.market_tick import MarketTick

# According to:
# https://www.binance.com/en/futures/ETHUSDT/calculator
# https://binance-docs.github.io/apidocs/futures/en/#new-order-trade
class Order:
    id: uuid.UUID
    type: OrderSide
    open_tick: MarketTick
    close_tick: MarketTick | None
    take_profit_to_price_ratio: float
    stop_loss_to_price_ratio: float

    def __init__(
        self,
        open_tick: MarketTick,
        type: OrderSide,
        take_profit_to_price_ratio: float,
        stop_loss_to_price_ratio: float,
    ):
        self.id = uuid.uuid4()
        self.type = type
        self.open_tick = open_tick
        self.close_tick = None
        self.take_profit_to_price_ratio = take_profit_to_price_ratio
        self.stop_loss_to_price_ratio = stop_loss_to_price_ratio

        if self.stop_loss_to_price_ratio > 0:
            raise ValueError(
                f"Order stop loss value should be <= 0,"
                + f" but was: ${self.stop_loss_to_price_ratio}."
            )

        if self.take_profit_to_price_ratio < 0:
            raise ValueError(
                f"Order take profit value should be >= 0,"
                + f" but was: ${self.take_profit_to_price_ratio}."
            )

    def is_open(self) -> bool:
        return self.close_tick == None

    def get_profit(self) -> float | None:
        return self._get_profit(self.close_tick)

    def close(self, tick: MarketTick):
        self.close_tick = tick

    def notify(self, new_tick: MarketTick):
        if not self.is_open():
            return

        if self._should_auto_close(new_tick):
            self.close(new_tick)

    def get_open_price(self) -> float:
        return (
            self.open_tick.bid_price
            if self.type == OrderSide.SELL
            else self.open_tick.ask_price
        )

    def get_close_price(self) -> float | None:
        return self._get_close_price(self.close_tick)

    def _get_close_price(self, possible_close_tick: MarketTick | None):
        if possible_close_tick == None:
            return None

        return (
            possible_close_tick.ask_price
            if self.type == OrderSide.SELL
            else possible_close_tick.bid_price
        )

    def _get_profit(self, possible_close_tick: MarketTick | None):
        close_price = self._get_close_price(possible_close_tick)

        if close_price == None:
            return None

        return (
            close_price - self.get_open_price()
            if self.type == OrderSide.BUY
            else self.get_open_price() - close_price
        )

    def _should_auto_close(self, new_tick: MarketTick):
        profit = self._get_profit(new_tick)
        assert profit is not None
        profit_ratio = profit / self.get_open_price()
        return (
            profit_ratio >= self.take_profit_to_price_ratio
            or profit_ratio <= self.stop_loss_to_price_ratio
        )
