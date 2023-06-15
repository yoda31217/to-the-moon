import pytest

from market.market_ticker import MarketTicker


class TestMarketTicker:
    def test_fields_are_correct_after_ticker_created(self):
        ticker = MarketTicker(100, 200.0, 300.0)

        assert ticker.timestamp == 100
        assert ticker.bid_price == 200.0
        assert ticker.ask_price == 300.0

    def test_raise_error_on_init_with_ask_price_equal_bid_price(self):
        with pytest.raises(ValueError):
            MarketTicker(100, 200.0, 200.0)
