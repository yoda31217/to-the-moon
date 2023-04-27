from order.order_side import OrderSide
from order.order import Order
from bot.bot import Bot
from market.market_ticker import MarketTicker


class BotOneStepOrder(Bot):
    check_point_tick: MarketTicker | None
    price_step_ratio: float
    take_profit_to_price_ratio: float
    stop_loss_to_price_ratio: float
    inverted: bool

    # TODO generify parameters and name generation, to be able to dinamicaly create them and report.
    def __init__(
        self,
        price_step_ratio: float,
        take_profit_to_price_ratio: float,
        stop_loss_to_price_ratio: float,
        inverted: bool,
    ) -> None:
        super().__init__(
            f'BotOneStepOrder'
            + f' [{price_step_ratio * 100:.2f}%'
            + f', {take_profit_to_price_ratio * 100:.2f}%'
            + f', {stop_loss_to_price_ratio * 100:.2f}%'
            + f', {"inverted" if inverted else "not inverted"}]'
        )
        self.check_point_tick = None
        self.price_step_ratio = price_step_ratio
        self.take_profit_to_price_ratio = take_profit_to_price_ratio
        self.stop_loss_to_price_ratio = stop_loss_to_price_ratio
        self.inverted = inverted

    def process_tick(
        self,
        new_tick: MarketTicker,
        orders: list[Order],
        closed_orders: list[Order],
    ):
        if self.check_point_tick is None:
            self.check_point_tick = new_tick
            # print(f"Initial checkpoint set at {tick.get_date_time()} and bid price: {tick.bid_price}")

        elif self.is_growth_step(new_tick):
            order_type = OrderSide.BUY if self.inverted else OrderSide.SELL
            orders.append(Order(new_tick, order_type, self.take_profit_to_price_ratio, self.stop_loss_to_price_ratio))
            self.check_point_tick = new_tick

        elif self.is_failing_step(new_tick):
            order_type = OrderSide.SELL if self.inverted else OrderSide.BUY
            orders.append(Order(new_tick, order_type, self.take_profit_to_price_ratio, self.stop_loss_to_price_ratio))
            self.check_point_tick = new_tick

    def is_growth_step(self, new_tick: MarketTicker):
        return (
            self.check_point_tick is not None
            and new_tick.bid_price
            >= self.check_point_tick.ask_price
            + self.check_point_tick.ask_price * self.price_step_ratio
        )

    def is_failing_step(self, new_tick: MarketTicker):
        return (
            self.check_point_tick is not None
            and new_tick.ask_price
            <= self.check_point_tick.bid_price
            - self.check_point_tick.bid_price * self.price_step_ratio
        )
