import pytest

from market.market_ticker import MarketTicker


class TestMarketTick:
    def test_fields_are_correct_after_tick_created(self):
        tick = MarketTicker(100, 200.0, 300.0)
        
        assert tick.timestamp == 100
        assert tick.bid_price == 200.0
        assert tick.ask_price == 300.0

    def test_raise_error_on_init_with_ask_price_equal_bid_price(self):
        with pytest.raises(ValueError):
            MarketTicker(100, 200.0, 200.0)
