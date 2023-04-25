from order.order_type import OrderType
from order.order import Order
from trade.trade_simulator_strategy import TradeSimulatorStrategy
from market.market_tick import MarketTick


class Bot0Strategy(TradeSimulatorStrategy):
    check_point_tick: MarketTick | None
    price_step_ratio: float
    inverted: bool

    def __init__(self, price_step_ratio: float, inverted: bool) -> None:
        super().__init__(
            f'Bot0[{price_step_ratio * 100:.2f}%, {"инвертирован" if inverted else "не инвертирован"}]'
        )
        self.check_point_tick = None
        self.price_step_ratio = price_step_ratio
        self.inverted = inverted

    def process_tick(
        self,
        new_tick: MarketTick,
        orders: list[Order],
        closed_orders: list[Order],
    ):
        if self.check_point_tick is None:
            self.check_point_tick = new_tick
            # print(f"Initial checkpoint set at {tick.get_date_time()} and bid price: {tick.bid_price}")

        elif self.is_growth_step(new_tick):
            order_type = OrderType.BUY if self.inverted else OrderType.SELL
            orders.append(Order(new_tick, order_type, self.price_step_ratio))
            self.check_point_tick = new_tick

        elif self.is_failing_step(new_tick):
            order_type = OrderType.SELL if self.inverted else OrderType.BUY
            orders.append(Order(new_tick, order_type, self.price_step_ratio))
            self.check_point_tick = new_tick

    def is_growth_step(self, new_tick: MarketTick):
        return (
            self.check_point_tick is not None
            and new_tick.bid_price
            >= self.check_point_tick.ask_price
            + self.check_point_tick.ask_price * self.price_step_ratio
        )

    def is_failing_step(self, new_tick: MarketTick):
        return (
            self.check_point_tick is not None
            and new_tick.ask_price
            <= self.check_point_tick.bid_price
            - self.check_point_tick.bid_price * self.price_step_ratio
        )
