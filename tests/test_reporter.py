import csv
from pathlib import Path

from src.models.schemas import VolatilityResult
from src.services.reporter import VolatilityReporter


def test_export_to_csv(tmp_path: Path):
    output_file = tmp_path / "test_out.csv"

    results = [
        VolatilityResult(
            base="BTC",
            quote="EUR",
            daily_volatility=3.3084702888119626,
            last_price=35617.08,
            average_volume=1694.0949196774188,
        ),
        VolatilityResult(
            base="ETH",
            quote="EUR",
            daily_volatility=3.1123116046847192,
            last_price=2360.35,
            average_volume=23870.74,
        ),
    ]

    dest = VolatilityReporter.export_to_csv(results, output_filepath=output_file)
    assert dest.exists()

    with open(dest, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        row1 = next(reader)
        row2 = next(reader)

    # Vérification stricte des colonnes selon les exigences du test
    assert header == ["base", "quote", "daily_volatility", "last_price", "average_volume"]
    assert row1 == ["BTC", "EUR", "3.3084702888119626", "35617.08", "1694.0949196774188"]
    assert row2 == ["ETH", "EUR", "3.1123116046847192", "2360.35", "23870.74"]
