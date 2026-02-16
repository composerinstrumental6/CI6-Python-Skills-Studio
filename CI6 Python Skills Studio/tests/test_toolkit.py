import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from toolkit import (
    cipher_transform,
    convert_fuel_consumption,
    convert_scientific_prefix,
    count_date_distance,
    get_fx_rate_with_fallback,
    summarize_text,
)


def test_summarize_text():
    result = summarize_text("Hello world. This is CS50!")
    assert result["characters"] == 26
    assert result["words"] == 5
    assert result["sentences"] == 2


def test_cipher_transform():
    assert cipher_transform("caesar", "encode", "abc XYZ", "2") == "cde ZAB"
    assert cipher_transform("caesar", "decode", "cde ZAB", "2") == "abc XYZ"
    assert cipher_transform("rot13", "encode", "hello") == "uryyb"
    assert cipher_transform("morse", "encode", "SOS") == "... --- ..."


def test_convert_fuel_consumption():
    assert convert_fuel_consumption(30, "mpg_us", "km_per_l") == 12.754311
    assert convert_fuel_consumption(12.754311, "km_per_l", "l_per_100km") == pytest.approx(7.840488)


def test_count_date_distance():
    result = count_date_distance("2026-02-16", "2026-03-05")
    assert result["target_weekday"] == "Thursday"
    assert result["delta_days"] == 17
    assert result["weeks"] == 2.43
    assert result["years"] == 0
    assert result["months"] == 0


def test_convert_scientific_prefix():
    converted, sci = convert_scientific_prefix(1, "mega", "giga")
    assert converted == 0.001
    assert "x 10^" in sci


def test_fx_rate_fallback_snapshot():
    rate, source, updated = get_fx_rate_with_fallback("USD", "EUR")
    assert rate > 0
    assert source in {"Yahoo Finance (live)", "Yahoo Finance (cached)", "Snapshot fallback"}
    assert isinstance(updated, str) and len(updated) >= 10
