from market.market_tick import MarketTick
from order.order import Order
from order.order_type import OrderType


class TestOrder:
    def test_fields_are_correct_after_order_created(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        order = Order(open_tick, OrderType.BUY, 0.5, 1.5)

        assert order.id != None
        assert order.type == OrderType.BUY
        assert order.open_tick == open_tick
        assert order.close_tick == None
        assert order.is_open
        assert order.take_profit_to_price_ratio == 0.5
        assert order.stop_loss_to_price_ratio == 1.5

    def test_get_profit_on_not_closed_return_none(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        order = Order(open_tick, OrderType.BUY, 0.5, 1.5)

        assert order.get_profit() == None

    def test_get_profit_on_buy_order_with_growth_return_currect_value(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        close_tick = MarketTick(200, 1200.0, 1300.0)
        order = Order(open_tick, OrderType.BUY, 0.5, 1.5)
        order.close(close_tick)

        assert order.get_profit() == 1200.0 - 300.0

    def test_get_profit_on_buy_order_with_falling_return_currect_value(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        close_tick = MarketTick(200, 100.0, 150.0)
        order = Order(open_tick, OrderType.BUY, 0.5, 1.5)
        order.close(close_tick)

        assert order.get_profit() == 100.0 - 300.0

    def test_get_profit_on_sell_order_with_growth_return_currect_value(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        close_tick = MarketTick(200, 1200.0, 1300.0)
        order = Order(open_tick, OrderType.SELL, 0.5, 1.5)
        order.close(close_tick)

        assert order.get_profit() == 200.0 - 1300.0

    def test_get_profit_on_sell_order_with_falling_return_currect_value(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        close_tick = MarketTick(200, 100.0, 150.0)
        order = Order(open_tick, OrderType.SELL, 0.5, 1.5)
        order.close(close_tick)

        assert order.get_profit() == 200.0 - 150.0

    def test_close_set_correct_close_tick(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        close_tick = MarketTick(200, 100.0, 150.0)
        order = Order(open_tick, OrderType.SELL, 0.5, 1.5)
        order.close(close_tick)

        assert order.close_tick == close_tick

    def test_is_open_after_close_return_false(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        close_tick = MarketTick(200, 100.0, 150.0)
        order = Order(open_tick, OrderType.SELL, 0.5, 1.5)
        order.close(close_tick)

        assert not order.is_open

    def test_get_open_price_on_buy_return_correct(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        order = Order(open_tick, OrderType.BUY, 0.5, 1.5)

        assert order.get_open_price() == 300.0

    def test_get_open_price_on_sell_return_correct(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        order = Order(open_tick, OrderType.SELL, 0.5, 1.5)

        assert order.get_open_price() == 200.0

    def test_get_close_price_on_open_return_none(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        order = Order(open_tick, OrderType.SELL, 0.5, 1.5)

        assert order.get_close_price() is None

    def test_get_close_price_on_buy_return_correct(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        close_tick = MarketTick(200, 100.0, 150.0)
        order = Order(open_tick, OrderType.BUY, 0.5, 1.5)
        order.close(close_tick)

        assert order.get_close_price() == 100.0

    def test_get_close_price_on_sell_return_correct(self):
        open_tick = MarketTick(100, 200.0, 300.0)
        close_tick = MarketTick(200, 100.0, 150.0)
        order = Order(open_tick, OrderType.SELL, 0.5, 1.5)
        order.close(close_tick)

        assert order.get_close_price() == 150.0
