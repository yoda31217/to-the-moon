from typing import cast
from simulator.order.order_side import OrderSide
from simulator.order.order import Order
from simulator.bot.bot import Bot, BotConfig
from simulator.market.market_ticker import MarketTicker


class BotGrid(Bot):
    check_point_ticker: MarketTicker | None
    step_to_price_ratio: float
    tp_to_entry_price_ratio: float
    sl_to_entry_price_ratio: float
    order_quantity: float
    order_leverage: float

    def __init__(self, config: BotConfig) -> None:
        super().__init__(config)

        self.check_point_ticker = None
        self.step_to_price_ratio = cast(float, config["step_to_price_ratio"])
        self.tp_to_entry_price_ratio = cast(float, config["tp_to_entry_price_ratio"])
        self.sl_to_entry_price_ratio = cast(float, config["sl_to_entry_price_ratio"])
        self.order_quantity = cast(float, config["order_quantity"])
        self.order_leverage = cast(float, config["order_leverage"])

    def process_ticker(
        self,
        new_ticker: MarketTicker,
        orders: list[Order],
        closed_orders: list[Order],
    ):
        if self.check_point_ticker is None:
            self.check_point_ticker = new_ticker

        elif self.was_price_changed_enough(new_ticker):
            orders.append(
                Order(
                    new_ticker,
                    OrderSide.BUY,
                    self.tp_to_entry_price_ratio,
                    self.sl_to_entry_price_ratio,
                    self.order_quantity,
                    self.order_leverage,
                )
            )
            orders.append(
                Order(
                    new_ticker,
                    OrderSide.SELL,
                    self.tp_to_entry_price_ratio,
                    self.sl_to_entry_price_ratio,
                    self.order_quantity,
                    self.order_leverage,
                )
            )
            self.check_point_ticker = new_ticker

    def was_price_changed_enough(self, new_ticker: MarketTicker):
        return self.check_point_ticker is not None and (
            new_ticker.bid_price
            >= self.check_point_ticker.ask_price
            + self.check_point_ticker.ask_price * self.step_to_price_ratio
            or new_ticker.ask_price
            <= self.check_point_ticker.bid_price
            - self.check_point_ticker.bid_price * self.step_to_price_ratio
        )
