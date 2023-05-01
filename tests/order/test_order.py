import pytest
from market.market_ticker import MarketTicker
from order.order import Order
from order.order_side import OrderSide


class TestOrder:
    def test_fields_are_correct_after_order_created(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.5, -1.5)

        assert order.id != None
        assert order.side == OrderSide.BUY
        assert order.entry_ticker == entry_ticker
        assert order.exit_ticker == None
        assert order.is_open()
        assert order.tp_to_entry_price_ratio == 0.5
        assert order.sl_to_entry_price_ratio == -1.5

    def test_throw_error_after_order_created_with_positive_sl(self):
        with pytest.raises(ValueError):
            Order(MarketTicker(100, 200.0, 300.0), OrderSide.BUY, 0.5, 1.5)

    def test_throw_error_after_order_created_with_negative_tp(self):
        with pytest.raises(ValueError):
            Order(MarketTicker(100, 200.0, 300.0), OrderSide.BUY, -0.5, -1.5)

    def test_get_initial_margin_on_buy_order_return_correct_value(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.5, -1.5)

        assert order.get_initial_margin() == 300.0

    def test_get_initial_margin_on_sell_order_return_correct_value(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)

        assert order.get_initial_margin() == 200.0

    def test_get_pnl_on_not_closed_buy_order_return_none(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.5, -1.5)

        assert order.get_pnl() == None

    def test_get_pnl_on_not_closed_sell_order_return_none(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)

        assert order.get_pnl() == None

    def test_get_pnl_with_new_ticker_on_not_closed_buy_order_return_correct(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.5, -1.5)

        new_ticker = MarketTicker(200, 1200.0, 1300.0)

        assert order.get_pnl(new_ticker) == 1200.0 - 300.0

    def test_get_pnl_with_new_ticker_on_not_closed_sell_order_return_none(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)

        new_ticker = MarketTicker(200, 100.0, 150.0)

        assert order.get_pnl(new_ticker) == 200.0 - 150.0

    def test_get_pnl_on_buy_closed_order_return_correct_value(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 1200.0, 1300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.5, -1.5)
        order.close(exit_ticker)

        assert order.get_pnl() == 1200.0 - 300.0

    def test_get_pnl_with_new_ticker_on_buy_closed_order_return_correct_value(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 1200.0, 1300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.5, -1.5)
        order.close(exit_ticker)

        new_ticker = MarketTicker(300, 2500.0, 2600.0)

        assert order.get_pnl(new_ticker) == 1200.0 - 300.0

    def test_get_pnl_on_sell_closed_order_return_correct_value(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 100.0, 150.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)
        order.close(exit_ticker)

        assert order.get_pnl() == 200.0 - 150.0

    def test_get_pnl_with_new_ticker_on_sell_closed_order_return_correct_value(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 100.0, 150.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)
        order.close(exit_ticker)

        new_ticker = MarketTicker(300, 50.0, 60.0)

        assert order.get_pnl(new_ticker) == 200.0 - 150.0

    def test_close_set_correct_exit_ticker(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 100.0, 150.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)
        order.close(exit_ticker)

        assert order.exit_ticker == exit_ticker

    def test_is_open_after_close_return_false(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 100.0, 150.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)
        order.close(exit_ticker)

        assert not order.is_open()

    def test_entry_price_on_buy_return_correct(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.5, -1.5)

        assert order.entry_price == 300.0

    def test_entry_price_on_sell_return_correct(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)

        assert order.entry_price == 200.0

    def test_get_exit_price_on_open_return_none(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)

        assert order.get_exit_price() is None

    def test_get_exit_price_on_buy_return_correct(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 100.0, 150.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.5, -1.5)
        order.close(exit_ticker)

        assert order.get_exit_price() == 100.0

    def test_get_exit_price_on_sell_return_correct(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 100.0, 150.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)
        order.close(exit_ticker)

        assert order.get_exit_price() == 150.0

    def test_do_not_close_buy_order_after_notify_with_less_than_tp(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.1, -999999)

        new_ticker = MarketTicker(200, 300.0 + 30.0 - 0.001, 500.0)

        order.notify(new_ticker)

        assert order.is_open()
        assert order.exit_ticker == None

    def test_do_close_buy_order_after_notify_with_equal_to_tp(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.1, -999999)

        new_ticker = MarketTicker(200, 300.0 + 30.0, 500.0)

        order.notify(new_ticker)

        assert not order.is_open()
        assert order.exit_ticker == new_ticker

    def test_do_not_close_buy_order_after_notify_with_more_than_sl(self):
        entry_ticker = MarketTicker(100, 299.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 999999, -0.1)

        new_ticker = MarketTicker(200, 300.0 - 30.0 + 0.001, 331.0)

        order.notify(new_ticker)

        assert order.is_open()
        assert order.exit_ticker == None

    def test_do_close_buy_order_after_notify_with_equal_to_sl(self):
        entry_ticker = MarketTicker(100, 299.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 999999, -0.1)

        new_ticker = MarketTicker(200, 300.0 - 30.0, 331.0)

        order.notify(new_ticker)

        assert not order.is_open()
        assert order.exit_ticker == new_ticker

    def test_do_not_close_sell_order_after_notify_with_less_than_tp(self):
        entry_ticker = MarketTicker(100, 220.0, 300.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.1, -999999)

        new_ticker = MarketTicker(200, 100.0, 220.0 - 22.0 + 0.001)

        order.notify(new_ticker)

        assert order.is_open()
        assert order.exit_ticker == None

    def test_do_close_sell_order_after_notify_with_equal_to_tp(self):
        entry_ticker = MarketTicker(100, 220.0, 300.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.1, -999999)

        new_ticker = MarketTicker(200, 100.0, 220.0 - 22.0)

        order.notify(new_ticker)

        assert not order.is_open()
        assert order.exit_ticker == new_ticker

    def test_do_not_close_sell_order_after_notify_with_more_than_sl(self):
        entry_ticker = MarketTicker(100, 220.0, 225.0)
        order = Order(entry_ticker, OrderSide.SELL, 999999, -0.1)

        new_ticker = MarketTicker(200, 240.0, 220.0 + 22.0 - 0.001)

        order.notify(new_ticker)

        assert order.is_open()
        assert order.exit_ticker == None

    def test_do_close_sell_order_after_notify_with_equal_to_sl(self):
        entry_ticker = MarketTicker(100, 220.0, 225.0)
        order = Order(entry_ticker, OrderSide.SELL, 999999, -0.1)

        new_ticker = MarketTicker(200, 240.0, 220.0 + 22.0)

        order.notify(new_ticker)

        assert not order.is_open()
        assert order.exit_ticker == new_ticker

    def test_do_not_auto_close_again_order_on_notify(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 100.0, 200.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.1, -999999)
        order.close(exit_ticker)

        new_ticker = MarketTicker(200, 500, 600.0)

        order.notify(new_ticker)

        assert not order.is_open()
        assert order.exit_ticker == exit_ticker

    def test_get_roe_on_open_return_none(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 999999, -999999)

        assert order.get_roe() is None

    def test_get_roe_on_closed_buy_order_return_correct_value(self):
        entry_ticker = MarketTicker(100, 90.0, 100.0)
        exit_ticker = MarketTicker(200, 120.0, 130.0)
        order = Order(entry_ticker, OrderSide.BUY, 999999, -999999)
        order.close(exit_ticker)

        assert order.get_roe() == 0.2

    def test_get_roe_on_closed_sell_order_return_correct_value(self):
        entry_ticker = MarketTicker(200, 100.0, 110.0)
        exit_ticker = MarketTicker(100, 70.0, 80.0)
        order = Order(entry_ticker, OrderSide.SELL, 999999, -999999)
        order.close(exit_ticker)

        assert order.get_roe() == 0.2
