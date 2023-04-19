import glob

import pandas as pd


def load_binance_k_lines(csv_files_pattern: str):
    csv_file_paths = glob.glob(csv_files_pattern)
    k_lines_data_frames = _load_binance_k_lines_data_frames(csv_file_paths)
    k_lines_data_frame = _join_binance_k_lines_data_frames(k_lines_data_frames)
    return k_lines_data_frame


def _join_binance_k_lines_data_frames(k_lines_data_frames):
    return pd.concat(k_lines_data_frames).sort_values(by=['openTimestampMillis'])


def _load_binance_k_lines_data_frames(csv_file_paths):
    return (_load_binance_k_lines_data_frame(csv_file_path) for csv_file_path in csv_file_paths)


def _load_binance_k_lines_data_frame(csv_file_path: str):
    return pd.read_csv(
        csv_file_path, sep=",", header=None,
        names=["openTimestampMillis", "openPrice", "highPrice", "lowPrice", "closePrice", "volume",
               "closeTimestampMillis", "quoteAssetVolume", "tradesCount", "takerBuyBaseAssetVolume",
               "takerBuyQuoteAssetVolume", "ignore"])
