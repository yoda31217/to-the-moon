from trade.trade_simulator_order import TradeSimulatorOrder
from trade.trade_simulator_order_type import TradeSimulatorOrderType
from trade.trade_simulator_strategy import TradeSimulatorStrategy
from trade.trade_simulator_tick import TradeSimulatorTick


class Bot0Strategy(TradeSimulatorStrategy):
    check_point_tick: TradeSimulatorTick | None
    price_step_ratio: float

    def __init__(self, price_step_ratio: float) -> None:
        super().__init__()
        self.check_point_tick = None
        self.price_step_ratio = price_step_ratio

    def process_tick(self, new_tick: TradeSimulatorTick,
                     orders: [TradeSimulatorOrder], closed_orders: [TradeSimulatorOrder]):
        if self.check_point_tick is None:
            self.check_point_tick = new_tick
            # print(f"Initial checkpoint set at {tick.get_date_time()} and bid price: {tick.bid_price}")

        elif self.is_growth_step(new_tick):
            orders.append(TradeSimulatorOrder(new_tick, TradeSimulatorOrderType.SELL, self.price_step_ratio))
            self.check_point_tick = new_tick

        elif self.is_failing_step(new_tick):
            orders.append(TradeSimulatorOrder(new_tick, TradeSimulatorOrderType.BUY, self.price_step_ratio))
            self.check_point_tick = new_tick

    def is_growth_step(self, new_tick: TradeSimulatorTick):
        return (new_tick.bid_price >=
                self.check_point_tick.ask_price + self.check_point_tick.ask_price * self.price_step_ratio)

    def is_failing_step(self, new_tick: TradeSimulatorTick):
        return (new_tick.ask_price <=
                self.check_point_tick.bid_price - self.check_point_tick.bid_price * self.price_step_ratio)
