from unittest.mock import patch

from src.cli import run_pipeline


@patch("src.cli.CryptoExchangeService")
@patch("src.cli.VolatilityReporter")
def test_main_cli_pipeline_success(mock_reporter, mock_exchange_service_class):
    mock_service = mock_exchange_service_class.return_value
    mock_service.fetch_fiat_pairs.return_value = ["BTC/EUR"]
    mock_service.fetch_ohlcv_candles.return_value = []

    # Exécution du pipeline CLI principal
    exit_code = run_pipeline(
        exchange_id="binance",
        quote_currency="EUR",
        days_period=30,
        output_file="test_out.csv",
    )

    # Comme aucune bougie n'est retournée, le pipeline avertit et sort avec le code 1
    assert exit_code == 1
    mock_service.fetch_fiat_pairs.assert_called_once_with(quote_currency="EUR")
