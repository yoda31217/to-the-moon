from datetime import date
import os
from typing import cast
from urllib.request import urlretrieve
import pandas as pd

from simulator.market.market_k_line import MarketKLinesDataFrame
from simulator.utils import data_frames


def load_k_lines(symbol: str, date_from: date, date_to: date) -> MarketKLinesDataFrame:
    if date_to < date_from:
        raise Exception(
            f"Date 'from'={date_from} cannot be greaterthan date 'to'={date_to}."
        )

    k_lines_data_frames = _load_k_lines_data_frames(symbol, date_from, date_to)
    k_lines_data_frame = _join_k_lines_data_frames(k_lines_data_frames)
    return k_lines_data_frame


def _join_k_lines_data_frames(
    k_lines_data_frames: list[MarketKLinesDataFrame],
) -> MarketKLinesDataFrame:
    return data_frames.sort_by(
        data_frames.concat(k_lines_data_frames), "open_timestamp_millis"
    )


def _load_k_lines_data_frames(
    symbol: str, date_from: date, date_to: date
) -> list[MarketKLinesDataFrame]:
    date_iso_strs: list[str] = (
        pd.date_range(date_from, date_to, freq="d")
        .strftime("%Y-%m-%d")
        .to_list()  # pyright: ignore [reportUnknownMemberType]
    )

    return [
        _load_k_lines_data_frame(symbol, date_iso_str) for date_iso_str in date_iso_strs
    ]


def _load_k_lines_data_frame(symbol: str, date_iso_str: str) -> MarketKLinesDataFrame:
    k_lines_file_path = _load_k_lines_to_file_if_needed(symbol, date_iso_str)
    return cast(
        MarketKLinesDataFrame,
        pd.read_csv(  # pyright: ignore [reportUnknownMemberType]
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
        ),
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
