import pytest
from market.market_ticker import MarketTicker
from order.order import Order
from order.order_side import OrderSide


class TestOrder:
    def test_throw_error_after_order_created_with_positive_sl(self):
        with pytest.raises(ValueError):
            Order(MarketTicker(100, 200.0, 300.0), OrderSide.BUY, 0.5, 1.5)

    def test_throw_error_after_order_created_with_negative_tp(self):
        with pytest.raises(ValueError):
            Order(MarketTicker(100, 200.0, 300.0), OrderSide.BUY, -0.5, -1.5)

    def test_calculate_possible_pnl_with_new_ticker_on_closed_order_return_already_calculated_value(
        self,
    ):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 1200.0, 1300.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.5, -1.5)
        order.close(exit_ticker)

        new_ticker = MarketTicker(300, 2500.0, 2600.0)

        assert order.calculate_possible_pnl(new_ticker) == 1200.0 - 300.0

    def test_do_not_auto_close_again_order_on_notify(self):
        entry_ticker = MarketTicker(100, 200.0, 300.0)
        exit_ticker = MarketTicker(200, 100.0, 200.0)
        order = Order(entry_ticker, OrderSide.BUY, 0.1, -999999)
        order.close(exit_ticker)

        new_ticker = MarketTicker(200, 500, 600.0)

        order.notify(new_ticker)

        assert not order.is_open
        assert order.exit_ticker == exit_ticker

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
        quantity,
        leverage,
        expected_entry_price,
        expected_exit_price,
        expected_initial_margin,
        expected_pnl,
        expected_roe,
        """,
        [
            (90, 100, 120, 130, OrderSide.BUY, 1, 1, 100, 120, 100, 20, 0.2),
            (90, 100, 120, 130, OrderSide.BUY, 0.1, 1, 100, 120, 10, 2, 0.2),
            (90, 100, 120, 130, OrderSide.BUY, 1, 2, 100, 120, 50, 20, 0.4),
            (90, 100, 120, 130, OrderSide.BUY, 0.1, 2, 100, 120, 5, 2, 0.4),
            (100, 110, 70, 80, OrderSide.SELL, 1, 1, 100, 80, 100, 20, 0.2),
            (100, 110, 70, 80, OrderSide.SELL, 0.1, 1, 100, 80, 10, 2, 0.2),
            (100, 110, 70, 80, OrderSide.SELL, 1, 2, 100, 80, 50, 20, 0.4),
            (100, 110, 70, 80, OrderSide.SELL, 0.1, 2, 100, 80, 5, 2, 0.4),
        ],
    )
    def test_all_fields_on_closed_order_are_correct(
        self,
        entry_ticker_bid_price: float,
        entry_ticker_ask_price: float,
        exit_ticker_bid_price: float,
        exit_ticker_ask_price: float,
        order_side: OrderSide,
        quantity: float,
        leverage: float,
        expected_entry_price: float,
        expected_exit_price: float,
        expected_initial_margin: float,
        expected_pnl: float,
        expected_roe: float,
    ):
        entry_ticker = MarketTicker(100, entry_ticker_bid_price, entry_ticker_ask_price)
        exit_ticker = MarketTicker(200, exit_ticker_bid_price, exit_ticker_ask_price)
        order = Order(entry_ticker, order_side, 999_999, -999_999, quantity, leverage)
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
        assert order.quantity == quantity
        assert order.leverage == leverage

    @pytest.mark.parametrize(
        """
        entry_ticker_bid_price,
        entry_ticker_ask_price,
        new_ticker_bid_price,
        new_ticker_ask_price,
        order_side,
        tp_to_entry_price_ratio,
        sl_to_entry_price_ratio,
        expected_is_open,
        """,
        [
            (200, 300, 329, 430, OrderSide.BUY, 0.1, -999, True),
            (200, 300, 330, 430, OrderSide.BUY, 0.1, -999, False),
            (200, 300, 271, 370, OrderSide.BUY, 999, -0.1, True),
            (200, 300, 270, 370, OrderSide.BUY, 999, -0.1, False),
            (200, 300, 80, 181, OrderSide.SELL, 0.1, -999, True),
            (200, 300, 80, 180, OrderSide.SELL, 0.1, -999, False),
            (200, 300, 120, 219, OrderSide.SELL, 999, -0.1, True),
            (200, 300, 120, 220, OrderSide.SELL, 999, -0.1, False),
        ],
    )
    def test_order_clossing_after_notify_is_correct(
        self,
        entry_ticker_bid_price: float,
        entry_ticker_ask_price: float,
        new_ticker_bid_price: float,
        new_ticker_ask_price: float,
        order_side: OrderSide,
        tp_to_entry_price_ratio: float,
        sl_to_entry_price_ratio: float,
        expected_is_open: bool,
    ):
        entry_ticker = MarketTicker(100, entry_ticker_bid_price, entry_ticker_ask_price)
        order = Order(
            entry_ticker, order_side, tp_to_entry_price_ratio, sl_to_entry_price_ratio
        )
        new_ticker = MarketTicker(200, new_ticker_bid_price, new_ticker_ask_price)
        order.notify(new_ticker)

        assert order.is_open == expected_is_open

    @pytest.mark.parametrize(
        """
        entry_ticker_bid_price,
        entry_ticker_ask_price,
        new_ticker_bid_price,
        new_ticker_ask_price,
        order_side,
        quantity,
        leverage,
        expected_possible_pnl,
        """,
        [
            (90, 100, 120, 130, OrderSide.BUY, 1, 1, 20),
            (90, 100, 120, 130, OrderSide.BUY, 0.1, 1, 2),
            (90, 100, 120, 130, OrderSide.BUY, 1, 2, 20),
            (90, 100, 120, 130, OrderSide.BUY, 0.1, 2, 2),
            (100, 110, 70, 80, OrderSide.SELL, 1, 1, 20),
            (100, 110, 70, 80, OrderSide.SELL, 0.1, 1, 2),
            (100, 110, 70, 80, OrderSide.SELL, 1, 2, 20),
            (100, 110, 70, 80, OrderSide.SELL, 0.1, 2, 2),
        ],
    )
    def test_calculate_possible_pnl_return_correct_value(
        self,
        entry_ticker_bid_price: float,
        entry_ticker_ask_price: float,
        new_ticker_bid_price: float,
        new_ticker_ask_price: float,
        order_side: OrderSide,
        quantity: float,
        leverage: float,
        expected_possible_pnl: float,
    ):
        entry_ticker = MarketTicker(100, entry_ticker_bid_price, entry_ticker_ask_price)
        order = Order(entry_ticker, order_side, 999_999, -999_999, quantity, leverage)

        new_ticker = MarketTicker(200, new_ticker_bid_price, new_ticker_ask_price)

        assert order.calculate_possible_pnl(new_ticker) == expected_possible_pnl
