from order.order_side import OrderSide
from order.order import Order
from bot.bot import Bot
from market.market_ticker import MarketTicker
from report.report_input import order_leverage


class BotOneStepOrder(Bot):
    check_point_ticker: MarketTicker | None
    step_to_price_ratio: float
    tp_to_entry_price_ratio: float
    sl_to_entry_price_ratio: float
    inverted: bool
    order_quantity: float
    order_leverage: float

    # TODO generify parameters and name generation,
    # to be able to dinamicaly create them and report.
    def __init__(self, config: dict) -> None:
        super().__init__(config)

        self.check_point_ticker = None
        self.step_to_price_ratio = config["step_to_price_ratio"]
        self.tp_to_entry_price_ratio = config["tp_to_entry_price_ratio"]
        self.sl_to_entry_price_ratio = config["sl_to_entry_price_ratio"]
        self.inverted = config["inverted"]
        self.order_quantity = config["order_quantity"]
        self.order_leverage = config["order_leverage"]

    def process_ticker(
        self,
        new_ticker: MarketTicker,
        orders: list[Order],
        closed_orders: list[Order],
    ):
        if self.check_point_ticker is None:
            self.check_point_ticker = new_ticker

        elif self.is_growth_step(new_ticker):
            order_side = OrderSide.BUY if self.inverted else OrderSide.SELL
            orders.append(
                Order(
                    new_ticker,
                    order_side,
                    self.tp_to_entry_price_ratio,
                    self.sl_to_entry_price_ratio,
                    self.order_quantity,
                    self.order_leverage,
                )
            )
            self.check_point_ticker = new_ticker

        elif self.is_failing_step(new_ticker):
            order_side = OrderSide.SELL if self.inverted else OrderSide.BUY
            orders.append(
                Order(
                    new_ticker,
                    order_side,
                    self.tp_to_entry_price_ratio,
                    self.sl_to_entry_price_ratio,
                    self.order_quantity,
                    self.order_leverage,
                )
            )
            self.check_point_ticker = new_ticker

    def is_growth_step(self, new_ticker: MarketTicker):
        return (
            self.check_point_ticker is not None
            and new_ticker.bid_price
            >= self.check_point_ticker.ask_price
            + self.check_point_ticker.ask_price * self.step_to_price_ratio
        )

    def is_failing_step(self, new_ticker: MarketTicker):
        return (
            self.check_point_ticker is not None
            and new_ticker.ask_price
            <= self.check_point_ticker.bid_price
            - self.check_point_ticker.bid_price * self.step_to_price_ratio
        )
