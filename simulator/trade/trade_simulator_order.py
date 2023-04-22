import uuid

from trade.trade_simulator_order_type import TradeSimulatorOrderType
from trade.trade_simulator_tick import TradeSimulatorTick


class TradeSimulatorOrder:
    id: uuid.UUID
    type: TradeSimulatorOrderType
    open_tick: TradeSimulatorTick
    close_tick: TradeSimulatorTick
    is_open: bool
    stop_loss_take_profit_ratio: float

    def __init__(self, tick: TradeSimulatorTick, type: TradeSimulatorOrderType, stop_loss_take_profit_ratio: float):
        self.id = uuid.uuid4()
        self.type = type
        self.open_tick = tick
        self.close_tick = None
        self.is_open = True
        self.stop_loss_take_profit_ratio = stop_loss_take_profit_ratio
        # print(f"New Order: {order.id} {order.open_tick.get_date_time()} {order.type} {order.get_open_price()}")

    def get_profit(self):
        return self._get_profit(self.close_tick)

    def close(self, tick: TradeSimulatorTick):
        self.close_tick = tick
        self.is_open = False
        # print(f"Close Order: {self.id} {self.close_tick.get_date_time()} {self.type} {self.get_close_price()}"
        #       + f" {self.get_profit()}")

    def notify(self, new_tick: TradeSimulatorTick):
        if not self.is_open:
            return

        if self._should_auto_close(new_tick):
            self.close(new_tick)

    def get_open_price(self):
        return (self.open_tick.bid_price
                if self.type == TradeSimulatorOrderType.SELL
                else self.open_tick.ask_price)

    def get_close_price(self):
        return self._get_close_price(self.close_tick)

    def _get_close_price(self, possible_close_tick: TradeSimulatorTick):
        return (possible_close_tick.ask_price
                if self.type == TradeSimulatorOrderType.SELL
                else possible_close_tick.bid_price)

    def _get_profit(self, possible_close_tick: TradeSimulatorTick):
        return (self._get_close_price(possible_close_tick) - self.get_open_price()
                if self.type == TradeSimulatorOrderType.BUY
                else self.get_open_price() - self._get_close_price(possible_close_tick))

    def _should_auto_close(self, new_tick: TradeSimulatorTick):
        profit = self._get_profit(new_tick)
        profit_ratio = profit / self.get_open_price()
        return abs(profit_ratio) >= self.stop_loss_take_profit_ratio
