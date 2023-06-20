from datetime import date
from numpy import float64
from pandas import DataFrame, Series, to_datetime


def target_action(prices: Series, price_increase_ratio: float):
    price_decrease_ratio = 1.0 - (price_increase_ratio - 1.0)

    price_0 = prices.iloc[0]
    increase_price = price_0 * price_increase_ratio
    decrease_price = price_0 * price_decrease_ratio

    for i in range(1, prices.shape[0]):
        price_i = prices.iloc[i]
        if price_i >= increase_price:
            return 1
        elif price_i <= decrease_price:
            return -1

    return 0


def calculate_target_action(prices: Series, window: int, price_increase_ratio: float):
    return (
        prices.shift(-window)
        .rolling(window + 1)
        .apply(target_action, args=(price_increase_ratio,))
    )


def calculate_and_set_target_action_feature(
    features: DataFrame, window: int, price_increase_ratio: float
):
    features["target_action"] = calculate_target_action(
        features["close_price"], window, price_increase_ratio
    )


def to_cleared_k_lines(raw_k_lines: DataFrame):
    k_lines = raw_k_lines[
        [
            # "open_price",
            # "low_price",
            # "high_price",
            "close_price",
            # "volume",
            # "trades_count"
        ]
    ]
    k_lines.index = to_datetime(raw_k_lines["open_timestamp_millis"], unit="ms")
    k_lines.index.name = "open_datetime"
    return k_lines


def validate_k_lines(
    k_lines: DataFrame, interval_date_from: date, interval_date_to: date
):
    validate_k_lines_rows_count(k_lines, interval_date_from, interval_date_to)

    validate_k_lines_no_na_cells(k_lines)
    validate_k_lines_no_null_cells(k_lines)

    validate_k_lines_positive_float_column(k_lines, "close_price")

    validate_k_lines_index_diff_is_60s(k_lines)


def validate_k_lines_index_diff_is_60s(k_lines):
    assert (
        (k_lines.index.to_series() - k_lines.index.to_series().shift(1))
        .iloc[1:]
        .dt.total_seconds()
        == 60
    ).all()


def validate_k_lines_positive_float_column(k_lines, name):
    assert k_lines.dtypes[name] == float64
    assert len(k_lines[k_lines[name] <= 0]) == 0


def validate_k_lines_no_null_cells(k_lines):
    assert len(k_lines[k_lines.isnull().any(axis=1)]) == 0


def validate_k_lines_no_na_cells(k_lines):
    assert len(k_lines[k_lines.isna().any(axis=1)]) == 0


def validate_k_lines_rows_count(
    k_lines, interval_date_from: date, interval_date_to: date
):
    assert len(k_lines) == calculate_interval_minutes(
        interval_date_from, interval_date_to
    )


def calculate_interval_minutes(interval_date_from: date, interval_date_to: date):
    return calculate_interval_hours(interval_date_from, interval_date_to) * 60.0


def calculate_interval_hours(interval_date_from, interval_date_to):
    return calculate_interval_days(interval_date_from, interval_date_to) * 24.0


def calculate_interval_days(interval_date_from, interval_date_to):
    return (interval_date_to - interval_date_from).days + 1.0
