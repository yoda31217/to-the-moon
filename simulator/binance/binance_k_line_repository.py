from datetime import date
import os
from urllib.request import urlretrieve
import pandas as pd

from k_line import KLinesDataFrame


def load_k_lines(symbol: str, date_from: date, date_to: date) -> KLinesDataFrame:
    if date_to < date_from:
        raise Exception(
            f"Date 'from'={date_from} cannot be greaterthan date 'to'={date_to}."
        )

    k_lines_data_frames = _load_k_lines_data_frames(symbol, date_from, date_to)
    k_lines_data_frame = _join_k_lines_data_frames(k_lines_data_frames)
    return k_lines_data_frame


def _join_k_lines_data_frames(
    k_lines_data_frames: list[KLinesDataFrame],
) -> KLinesDataFrame:
    return pd.concat(k_lines_data_frames).sort_values(by=["open_timestamp_millis"])


def _load_k_lines_data_frames(
    symbol: str, date_from: date, date_to: date
) -> list[KLinesDataFrame]:
    date_iso_strs: list[str] = (
        pd.date_range(date_from, date_to, freq="d").strftime("%Y-%m-%d").to_list()
    )

    if len(date_iso_strs) > 31:
        raise Exception(f"Date 'from' - 'to' interval should be <= 31 days.")

    return [
        _load_k_lines_data_frame(symbol, date_iso_str) for date_iso_str in date_iso_strs
    ]


def _load_k_lines_data_frame(symbol: str, date_iso_str: str) -> KLinesDataFrame:
    k_lines_file_path = _load_k_lines_to_file_if_needed(symbol, date_iso_str)
    return pd.read_csv(
        k_lines_file_path,
        sep=",",
        header=0,
        names=[
            "open_timestamp_millis",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "volume",
            "close_timestamp_millis",
            "quote_asset_volume",
            "trades_count",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ],
    )


def _load_k_lines_to_file_if_needed(symbol: str, date_iso_str: str) -> str:
    file_path = (
        f"./data/futures/um/daily/klines/{symbol}/1m/{symbol}-1m-{date_iso_str}.zip"
    )

    if os.path.isfile(file_path):
        return file_path

    _load_k_lines_to_file(symbol, date_iso_str, file_path)
    return file_path


# https://www.binance.com/en/landing/data
def _load_k_lines_to_file(symbol: str, date_iso_str: str, file_path: str):
    url = (
        f"https://data.binance.vision"
        + f"/data/futures/um/daily/klines/{symbol}/1m/{symbol}-1m-{date_iso_str}.zip"
    )
    try:
        urlretrieve(url, file_path)
    except Exception as e:
        raise Exception(f"No Binance data for {symbol}:{date_iso_str}.") from e
