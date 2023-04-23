import glob

import pandas as pd
import streamlit as st


@st.cache_data
def load_binance_k_lines_with_cache(symbol: str, iso_date_str: str) -> pd.DataFrame:
    return _load_binance_k_lines_data_frame(
        f"https://data.binance.vision/data/spot/daily/klines/{symbol}/1s/{symbol}-1s-{iso_date_str}.zip"
    )


def load_binance_k_lines(csv_files_pattern: str):
    csv_file_paths = glob.glob(csv_files_pattern)
    k_lines_data_frames = _load_binance_k_lines_data_frames(csv_file_paths)
    k_lines_data_frame = _join_binance_k_lines_data_frames(k_lines_data_frames)
    return k_lines_data_frame


def _join_binance_k_lines_data_frames(k_lines_data_frames):
    return pd.concat(k_lines_data_frames).sort_values(by=["open_timestamp_millis"])


def _load_binance_k_lines_data_frames(csv_file_paths):
    return (
        _load_binance_k_lines_data_frame(csv_file_path)
        for csv_file_path in csv_file_paths
    )


def _load_binance_k_lines_data_frame(csv_file_path: str):
    return pd.read_csv(
        csv_file_path,
        sep=",",
        header=None,
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
