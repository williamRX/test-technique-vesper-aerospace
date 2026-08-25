from src.config import Settings


def test_default_settings():
    s = Settings()
    assert s.EXCHANGE.lower() == "binance"
    assert s.QUOTE_CURRENCY == "EUR"
    assert s.DAYS_PERIOD == 30
    assert s.OUTPUT_FILE == "crypto_volatility.csv"
    assert s.STRICT_DATA_CHECK is True


def test_custom_settings_override():
    s = Settings(
        EXCHANGE="coinbase",
        QUOTE_CURRENCY="USD",
        DAYS_PERIOD=15,
        OUTPUT_FILE="custom_out.csv",
    )
    assert s.EXCHANGE == "coinbase"
    assert s.QUOTE_CURRENCY == "USD"
    assert s.DAYS_PERIOD == 15
    assert s.OUTPUT_FILE == "custom_out.csv"
