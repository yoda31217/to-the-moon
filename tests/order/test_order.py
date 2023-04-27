import pytest
from market.market_ticker import MarketTicker
from order.order import Order
from order.order_side import OrderSide


class TestOrder:
    def test_fields_are_correct_after_order_created(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        order = Order(open_tick, OrderSide.BUY, 0.5, -1.5)

        assert order.id != None
        assert order.side == OrderSide.BUY
        assert order.entry_ticker == open_tick
        assert order.exit_ticker == None
        assert order.is_open()
        assert order.tp_to_entry_price_ratio == 0.5
        assert order.sl_to_entry_price_ratio == -1.5

    def test_throw_error_after_order_created_with_positive_stoploss(self):
        with pytest.raises(ValueError):
            Order(MarketTicker(100, 200.0, 300.0), OrderSide.BUY, 0.5, 1.5)

    def test_throw_error_after_order_created_with_negative_takeprofit(self):
        with pytest.raises(ValueError):
            Order(MarketTicker(100, 200.0, 300.0), OrderSide.BUY, -0.5, -1.5)

    def test_get_profit_on_not_closed_return_none(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        order = Order(open_tick, OrderSide.BUY, 0.5, -1.5)

        assert order.get_pnl() == None

    def test_get_profit_on_buy_order_with_growth_return_currect_value(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        close_tick = MarketTicker(200, 1200.0, 1300.0)
        order = Order(open_tick, OrderSide.BUY, 0.5, -1.5)
        order.close(close_tick)

        assert order.get_pnl() == 1200.0 - 300.0

    def test_get_profit_on_buy_order_with_falling_return_currect_value(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        close_tick = MarketTicker(200, 100.0, 150.0)
        order = Order(open_tick, OrderSide.BUY, 0.5, -1.5)
        order.close(close_tick)

        assert order.get_pnl() == 100.0 - 300.0

    def test_get_profit_on_sell_order_with_growth_return_currect_value(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        close_tick = MarketTicker(200, 1200.0, 1300.0)
        order = Order(open_tick, OrderSide.SELL, 0.5, -1.5)
        order.close(close_tick)

        assert order.get_pnl() == 200.0 - 1300.0

    def test_get_profit_on_sell_order_with_falling_return_currect_value(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        close_tick = MarketTicker(200, 100.0, 150.0)
        order = Order(open_tick, OrderSide.SELL, 0.5, -1.5)
        order.close(close_tick)

        assert order.get_pnl() == 200.0 - 150.0

    def test_close_set_correct_close_tick(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        close_tick = MarketTicker(200, 100.0, 150.0)
        order = Order(open_tick, OrderSide.SELL, 0.5, -1.5)
        order.close(close_tick)

        assert order.exit_ticker == close_tick

    def test_is_open_after_close_return_false(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        close_tick = MarketTicker(200, 100.0, 150.0)
        order = Order(open_tick, OrderSide.SELL, 0.5, -1.5)
        order.close(close_tick)

        assert not order.is_open()

    def test_get_open_price_on_buy_return_correct(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        order = Order(open_tick, OrderSide.BUY, 0.5, -1.5)

        assert order.get_entry_price() == 300.0

    def test_get_open_price_on_sell_return_correct(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        order = Order(open_tick, OrderSide.SELL, 0.5, -1.5)

        assert order.get_entry_price() == 200.0

    def test_get_close_price_on_open_return_none(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        order = Order(open_tick, OrderSide.SELL, 0.5, -1.5)

        assert order.get_exit_price() is None

    def test_get_close_price_on_buy_return_correct(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        close_tick = MarketTicker(200, 100.0, 150.0)
        order = Order(open_tick, OrderSide.BUY, 0.5, -1.5)
        order.close(close_tick)

        assert order.get_exit_price() == 100.0

    def test_get_close_price_on_sell_return_correct(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        close_tick = MarketTicker(200, 100.0, 150.0)
        order = Order(open_tick, OrderSide.SELL, 0.5, -1.5)
        order.close(close_tick)

        assert order.get_exit_price() == 150.0

    def test_do_not_close_buy_order_after_notify_with_less_than_take_profit(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        order = Order(open_tick, OrderSide.BUY, 0.1, -999999)

        new_tick = MarketTicker(200, 300.0 + 30.0 - 0.001, 500.0)

        order.notify(new_tick)

        assert order.is_open()
        assert order.exit_ticker == None

    def test_do_close_buy_order_after_notify_with_equal_to_take_profit(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        order = Order(open_tick, OrderSide.BUY, 0.1, -999999)

        new_tick = MarketTicker(200, 300.0 + 30.0, 500.0)

        order.notify(new_tick)

        assert not order.is_open()
        assert order.exit_ticker == new_tick

    def test_do_not_close_buy_order_after_notify_with_more_than_stop_loss(self):
        open_tick = MarketTicker(100, 299.0, 300.0)
        order = Order(open_tick, OrderSide.BUY, 999999, -0.1)

        new_tick = MarketTicker(200, 300.0 - 30.0 + 0.001, 331.0)

        order.notify(new_tick)

        assert order.is_open()
        assert order.exit_ticker == None

    def test_do_close_buy_order_after_notify_with_equal_to_stop_loss(self):
        open_tick = MarketTicker(100, 299.0, 300.0)
        order = Order(open_tick, OrderSide.BUY, 999999, -0.1)

        new_tick = MarketTicker(200, 300.0 - 30.0, 331.0)

        order.notify(new_tick)

        assert not order.is_open()
        assert order.exit_ticker == new_tick

    def test_do_not_close_sell_order_after_notify_with_less_than_take_profit(self):
        open_tick = MarketTicker(100, 220.0, 300.0)
        order = Order(open_tick, OrderSide.SELL, 0.1, -999999)

        new_tick = MarketTicker(200, 100.0, 220.0 - 22.0 + 0.001)

        order.notify(new_tick)

        assert order.is_open()
        assert order.exit_ticker == None

    def test_do_close_sell_order_after_notify_with_equal_to_take_profit(self):
        open_tick = MarketTicker(100, 220.0, 300.0)
        order = Order(open_tick, OrderSide.SELL, 0.1, -999999)

        new_tick = MarketTicker(200, 100.0, 220.0 - 22.0)

        order.notify(new_tick)

        assert not order.is_open()
        assert order.exit_ticker == new_tick

    def test_do_not_close_sell_order_after_notify_with_more_than_stop_loss(self):
        open_tick = MarketTicker(100, 220.0, 225.0)
        order = Order(open_tick, OrderSide.SELL, 999999, -0.1)

        new_tick = MarketTicker(200, 240.0, 220.0 + 22.0 - 0.001)

        order.notify(new_tick)

        assert order.is_open()
        assert order.exit_ticker == None

    def test_do_close_sell_order_after_notify_with_equal_to_stop_loss(self):
        open_tick = MarketTicker(100, 220.0, 225.0)
        order = Order(open_tick, OrderSide.SELL, 999999, -0.1)

        new_tick = MarketTicker(200, 240.0, 220.0 + 22.0)

        order.notify(new_tick)

        assert not order.is_open()
        assert order.exit_ticker == new_tick

    def test_do_not_auto_close_again_order_on_notify(self):
        open_tick = MarketTicker(100, 200.0, 300.0)
        close_tick = MarketTicker(200, 100.0, 200.0)
        order = Order(open_tick, OrderSide.BUY, 0.1, -999999)
        order.close(close_tick)

        new_tick = MarketTicker(200, 500, 600.0)

        order.notify(new_tick)

        assert not order.is_open()
        assert order.exit_ticker == close_tick
