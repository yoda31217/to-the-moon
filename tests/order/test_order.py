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
        assert order.is_open
        assert order.tp_to_entry_price_ratio == 0.5
        assert order.sl_to_entry_price_ratio == -1.5

    def test_throw_error_after_order_created_with_positive_sl(self):
        with pytest.raises(ValueError):
            Order(MarketTicker(100, 200.0, 300.0), OrderSide.BUY, 0.5, 1.5)

    def test_throw_error_after_order_created_with_negative_tp(self):
        with pytest.raises(ValueError):
            Order(MarketTicker(100, 200.0, 300.0), OrderSide.BUY, -0.5, -1.5)

    def test_pnl_on_not_closed_buy_order_return_none(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.5, -1.5)

        assert order.pnl == None

    def test_pnl_on_not_closed_sell_order_return_none(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)

        assert order.pnl == None

    def test_calculate_possible_pnl_with_new_ticker_on_not_closed_buy_order_return_correct(
        self,
    ):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.5, -1.5)

        new_ticker = MarketTicker(200, 1200.0, 1300.0)

        assert order.calculate_possible_pnl(new_ticker) == 1200.0 - 300.0

    def test_calculate_possible_pnl_with_new_ticker_on_not_closed_sell_order_return_none(
        self,
    ):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)

        new_ticker = MarketTicker(200, 100.0, 150.0)

        assert order.calculate_possible_pnl(new_ticker) == 200.0 - 150.0

    def test_calculate_possible_pnl_with_new_ticker_on_buy_closed_order_return_correct_value(
        self,
    ):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 1200.0, 1300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.5, -1.5)
        order.close(exit_ticker)

        new_ticker = MarketTicker(300, 2500.0, 2600.0)

        assert order.calculate_possible_pnl(new_ticker) == 1200.0 - 300.0

    def test_calculate_possible_pnl_with_new_ticker_on_sell_closed_order_return_correct_value(
        self,
    ):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 100.0, 150.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)
        order.close(exit_ticker)

        new_ticker = MarketTicker(300, 50.0, 60.0)

        assert order.calculate_possible_pnl(new_ticker) == 200.0 - 150.0

    def test_exit_price_on_open_return_none(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.5, -1.5)

        assert order.exit_price is None

    def test_do_not_close_buy_order_after_notify_with_less_than_tp(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.1, -999999)

        new_ticker = MarketTicker(200, 300.0 + 30.0 - 0.001, 500.0)

        order.notify(new_ticker)

        assert order.is_open
        assert order.exit_ticker == None

    def test_do_close_buy_order_after_notify_with_equal_to_tp(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.1, -999999)

        new_ticker = MarketTicker(200, 300.0 + 30.0, 500.0)

        order.notify(new_ticker)

        assert not order.is_open
        assert order.exit_ticker == new_ticker

    def test_do_not_close_buy_order_after_notify_with_more_than_sl(self):
        entry_ticker = MarketTicker(100, 299.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 999999, -0.1)

        new_ticker = MarketTicker(200, 300.0 - 30.0 + 0.001, 331.0)

        order.notify(new_ticker)

        assert order.is_open
        assert order.exit_ticker == None

    def test_do_close_buy_order_after_notify_with_equal_to_sl(self):
        entry_ticker = MarketTicker(100, 299.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 999999, -0.1)

        new_ticker = MarketTicker(200, 300.0 - 30.0, 331.0)

        order.notify(new_ticker)

        assert not order.is_open
        assert order.exit_ticker == new_ticker

    def test_do_not_close_sell_order_after_notify_with_less_than_tp(self):
        entry_ticker = MarketTicker(100, 220.0, 300.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.1, -999999)

        new_ticker = MarketTicker(200, 100.0, 220.0 - 22.0 + 0.001)

        order.notify(new_ticker)

        assert order.is_open
        assert order.exit_ticker == None

    def test_do_close_sell_order_after_notify_with_equal_to_tp(self):
        entry_ticker = MarketTicker(100, 220.0, 300.0)
        order = Order(entry_ticker, OrderSide.SELL, 0.1, -999999)

        new_ticker = MarketTicker(200, 100.0, 220.0 - 22.0)

        order.notify(new_ticker)

        assert not order.is_open
        assert order.exit_ticker == new_ticker

    def test_do_not_close_sell_order_after_notify_with_more_than_sl(self):
        entry_ticker = MarketTicker(100, 220.0, 225.0)
        order = Order(entry_ticker, OrderSide.SELL, 999999, -0.1)

        new_ticker = MarketTicker(200, 240.0, 220.0 + 22.0 - 0.001)

        order.notify(new_ticker)

        assert order.is_open
        assert order.exit_ticker == None

    def test_do_close_sell_order_after_notify_with_equal_to_sl(self):
        entry_ticker = MarketTicker(100, 220.0, 225.0)
        order = Order(entry_ticker, OrderSide.SELL, 999999, -0.1)

        new_ticker = MarketTicker(200, 240.0, 220.0 + 22.0)

        order.notify(new_ticker)

        assert not order.is_open
        assert order.exit_ticker == new_ticker

    def test_do_not_auto_close_again_order_on_notify(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 100.0, 200.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.1, -999999)
        order.close(exit_ticker)

        new_ticker = MarketTicker(200, 500, 600.0)

        order.notify(new_ticker)

        assert not order.is_open
        assert order.exit_ticker == exit_ticker

    def test_roe_on_open_return_none(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        order = Order(entry_ticker, OrderSide.BUY, 999999, -999999)

        assert order.roe is None

    @pytest.mark.parametrize(
        """
        entry_ticker_bid_price,
        entry_ticker_ask_price,
        order_side,
        expected_entry_price,
        expected_initial_margin,
        """,
        [
            (90, 100, OrderSide.BUY, 100, 100),
            (100, 110, OrderSide.SELL, 100, 100),
        ],
    )
    def test_all_fields_on_open_order_are_correct(
        self,
        entry_ticker_bid_price: float,
        entry_ticker_ask_price: float,
        order_side: OrderSide,
        expected_entry_price: float,
        expected_initial_margin: float,
    ):
        entry_ticker = MarketTicker(100, entry_ticker_bid_price, entry_ticker_ask_price)
        order = Order(entry_ticker, order_side, 999_999, -999_999)

        assert order.roe == None
        assert order.initial_margin == expected_initial_margin
        assert order.pnl == None
        assert order.is_open
        assert order.entry_price == expected_entry_price
        assert order.exit_price == None
        assert order.entry_ticker == entry_ticker
        assert order.exit_ticker == None
        assert order.side == order_side
        assert order.id != None
        assert order.tp_to_entry_price_ratio == 999_999
        assert order.sl_to_entry_price_ratio == -999_999

    @pytest.mark.parametrize(
        """
        entry_ticker_bid_price,
        entry_ticker_ask_price,
        exit_ticker_bid_price,
        exit_ticker_ask_price,
        order_side,
        expected_entry_price,
        expected_exit_price,
        expected_initial_margin,
        expected_pnl,
        expected_roe,
        """,
        [
            (90, 100, 120, 130, OrderSide.BUY, 100, 120, 100, 20, 0.2),
            (100, 110, 70, 80, OrderSide.SELL, 100, 80, 100, 20, 0.2),
        ],
    )
    def test_all_fields_on_closed_order_are_correct(
        self,
        entry_ticker_bid_price: float,
        entry_ticker_ask_price: float,
        exit_ticker_bid_price: float,
        exit_ticker_ask_price: float,
        order_side: OrderSide,
        expected_entry_price: float,
        expected_exit_price: float,
        expected_initial_margin: float,
        expected_pnl: float,
        expected_roe: float,
    ):
        entry_ticker = MarketTicker(100, entry_ticker_bid_price, entry_ticker_ask_price)
        exit_ticker = MarketTicker(200, exit_ticker_bid_price, exit_ticker_ask_price)
        order = Order(entry_ticker, order_side, 999_999, -999_999)
        order.close(exit_ticker)

        assert order.roe == expected_roe
        assert order.initial_margin == expected_initial_margin
        assert order.pnl == expected_pnl
        assert not order.is_open
        assert order.entry_price == expected_entry_price
        assert order.exit_price == expected_exit_price
        assert order.entry_ticker == entry_ticker
        assert order.exit_ticker == exit_ticker
        assert order.side == order_side
        assert order.id != None
        assert order.tp_to_entry_price_ratio == 999_999
        assert order.sl_to_entry_price_ratio == -999_999
