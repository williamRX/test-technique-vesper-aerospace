import math

import pytest

from src.models.schemas import MarketCandle
from src.services.metrics import (
    calculate_daily_returns,
    calculate_daily_volatility,
    calculate_sample_variance,
    compute_pair_metrics,
)


def test_calculate_daily_returns():
    prices = [100.0, 110.0, 121.0]
    returns = calculate_daily_returns(prices)
    assert len(returns) == 2
    assert pytest.approx(returns[0]) == 0.10
    assert pytest.approx(returns[1]) == 0.10


def test_calculate_sample_variance_and_volatility():
    # R_1 = 0.10, R_2 = -0.10
    # Mean = 0.0
    # Variance = [(0.10 - 0)^2 + (-0.10 - 0)^2] / (2 - 1) = 0.02
    # Daily Volatility = sqrt(0.02)
    prices = [100.0, 110.0, 99.0]
    returns = calculate_daily_returns(prices)
    assert len(returns) == 2

    variance = calculate_sample_variance(returns)
    assert pytest.approx(variance) == 0.02

    volatility = calculate_daily_volatility(returns)
    assert pytest.approx(volatility) == math.sqrt(0.02)


def test_compute_pair_metrics_valid():
    # 3 bougies fictives
    candles = [
        MarketCandle(timestamp=1, open=100.0, high=105.0, low=95.0, close=100.0, volume=1000.0),
        MarketCandle(timestamp=2, open=100.0, high=115.0, low=98.0, close=110.0, volume=2000.0),
        MarketCandle(timestamp=3, open=110.0, high=112.0, low=95.0, close=99.0, volume=3000.0),
    ]

    res = compute_pair_metrics(
        symbol="BTC/EUR",
        candles=candles,
        required_days=3,
        strict_check=True,
    )

    assert res is not None
    assert res.base == "BTC"
    assert res.quote == "EUR"
    assert res.last_price == 99.0
    assert res.average_volume == 2000.0  # (1000 + 2000 + 3000) / 3
    assert pytest.approx(res.daily_volatility) == math.sqrt(0.02)


def test_compute_pair_metrics_strict_option_a_ignored():
    # 2 bougies disponibles alors que 5 sont requises
    candles = [
        MarketCandle(timestamp=1, open=100.0, high=105.0, low=95.0, close=100.0, volume=1000.0),
        MarketCandle(timestamp=2, open=100.0, high=115.0, low=98.0, close=110.0, volume=2000.0),
    ]

    # Option A: Strict Check -> Retounrne None car 2 < 5
    res = compute_pair_metrics(
        symbol="BTC/EUR",
        candles=candles,
        required_days=5,
        strict_check=True,
    )

    assert res is None
