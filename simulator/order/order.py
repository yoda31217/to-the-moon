import uuid

from order.order_type import OrderType
from market.market_tick import MarketTick


class Order:
    id: uuid.UUID
    type: OrderType
    open_tick: MarketTick
    close_tick: MarketTick | None
    # TODO remove this field
    is_open: bool
    take_profit_to_price_ratio: float
    stop_loss_to_price_ratio: float

    def __init__(
        self,
        open_tick: MarketTick,
        type: OrderType,
        take_profit_to_price_ratio: float,
        stop_loss_to_price_ratio: float,
    ):
        self.id = uuid.uuid4()
        self.type = type
        self.open_tick = open_tick
        self.close_tick = None
        self.is_open = True
        self.take_profit_to_price_ratio = take_profit_to_price_ratio
        self.stop_loss_to_price_ratio = stop_loss_to_price_ratio

    def get_profit(self) -> float | None:
        return self._get_profit(self.close_tick)

    def close(self, tick: MarketTick):
        self.close_tick = tick
        self.is_open = False
        # print(f"Close Order: {self.id} {self.close_tick.get_date_time()} {self.type} {self.get_close_price()}"
        #       + f" {self.get_profit()}")

    def notify(self, new_tick: MarketTick):
        if not self.is_open:
            return

        if self._should_auto_close(new_tick):
            self.close(new_tick)

    def get_open_price(self) -> float:
        return (
            self.open_tick.bid_price
            if self.type == OrderType.SELL
            else self.open_tick.ask_price
        )

    def get_close_price(self) -> float | None:
        return self._get_close_price(self.close_tick)

    def _get_close_price(self, possible_close_tick: MarketTick | None):
        if possible_close_tick == None:
            return None

        return (
            possible_close_tick.ask_price
            if self.type == OrderType.SELL
            else possible_close_tick.bid_price
        )

    def _get_profit(self, possible_close_tick: MarketTick | None):
        close_price = self._get_close_price(possible_close_tick)

        if close_price == None:
            return None

        return (
            close_price - self.get_open_price()
            if self.type == OrderType.BUY
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
