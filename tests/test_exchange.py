from unittest.mock import MagicMock, patch

from src.services.exchange import CryptoExchangeService


@patch("ccxt.binance")
def test_exchange_service_init_and_fetch_fiat_pairs(mock_binance_class):
    mock_client = MagicMock()
    mock_binance_class.return_value = mock_client

    mock_client.load_markets.return_value = {
        "BTC/EUR": {"symbol": "BTC/EUR", "quote": "EUR", "active": True, "spot": True},
        "ETH/EUR": {"symbol": "ETH/EUR", "quote": "EUR", "active": True, "spot": True},
        "BTC/USDT": {"symbol": "BTC/USDT", "quote": "USDT", "active": True, "spot": True},
        "SOL/EUR": {"symbol": "SOL/EUR", "quote": "EUR", "active": False, "spot": True},  # inactif
    }

    service = CryptoExchangeService(exchange_id="binance")
    pairs = service.fetch_fiat_pairs(quote_currency="EUR")

    assert pairs == ["BTC/EUR", "ETH/EUR"]


@patch("ccxt.binance")
def test_fetch_ohlcv_candles_conversion(mock_binance_class):
    mock_client = MagicMock()
    mock_binance_class.return_value = mock_client

    # Format brut CCXT: [timestamp, open, high, low, close, volume]
    mock_client.fetch_ohlcv.return_value = [
        [1600000000000, 100.0, 105.0, 95.0, 102.0, 500.0],
        [1600086400000, 102.0, 110.0, 101.0, 108.0, 750.0],
    ]

    service = CryptoExchangeService(exchange_id="binance")
    candles = service.fetch_ohlcv_candles("BTC/EUR", days_period=2)

    assert len(candles) == 2
    assert candles[0].timestamp == 1600000000000
    assert candles[0].close == 102.0
    assert candles[1].volume == 750.0
