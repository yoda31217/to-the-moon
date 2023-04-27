from datetime import date
import os
from urllib.request import urlretrieve
import pandas as pd


def load_binance_k_lines(symbol: str, date_from: date, date_to: date) -> pd.DataFrame:
    if date_to < date_from:
        raise Exception(
            f"'Дата с' {date_from} не может быть больше 'Дата по' {date_to}."
        )

    k_lines_data_frames = _load_binance_k_lines_data_frames(symbol, date_from, date_to)
    k_lines_data_frame = _join_binance_k_lines_data_frames(k_lines_data_frames)
    return k_lines_data_frame


def _join_binance_k_lines_data_frames(
    k_lines_data_frames: list[pd.DataFrame],
) -> pd.DataFrame:
    return pd.concat(k_lines_data_frames).sort_values(by=["open_timestamp_millis"])


def _load_binance_k_lines_data_frames(
    symbol: str, date_from: date, date_to: date
) -> list[pd.DataFrame]:
    date_iso_strs = (
        pd.date_range(date_from, date_to, freq="d").strftime("%Y-%m-%d").to_list()
    )

    if len(date_iso_strs) > 31:
        raise Exception(f"Интервал симуляции не может превышать 31 день.")

    return [
        _load_binance_k_lines_data_frame(symbol, date_iso_str)
        for date_iso_str in date_iso_strs
    ]


def _load_binance_k_lines_data_frame(symbol: str, date_iso_str: str):
    k_lines_file_path = _load_binance_k_lines_to_file_if_needed(symbol, date_iso_str)
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


def _load_binance_k_lines_to_file_if_needed(symbol, date_iso_str) -> str:
    file_path = f"./data/{symbol}-1s-{date_iso_str}.zip"
    file_path = (
        f"./data/futures/um/daily/klines/{symbol}/1m/{symbol}-1m-{date_iso_str}.zip"
    )
    if os.path.isfile(file_path):
        return file_path
    _load_binance_k_lines_to_file(symbol, date_iso_str, file_path)
    return file_path


def _load_binance_k_lines_to_file(symbol, date_iso_str, file_path):
    try:
        urlretrieve(
            f"https://data.binance.vision/data/futures/um/daily/klines/{symbol}/1m/{symbol}-1m-{date_iso_str}.zip",
            file_path,
        )
    except Exception as e:
        raise Exception(
            f"Нет архивных данных по ценам для символа {symbol} на дату {date_iso_str}."
        ) from e


BINANCE_SYMBOLS = ["ETHUSDT", "BTCUSDT"]
