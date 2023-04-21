import datetime as dt

import pandas as pd
import seaborn as sns

sns.set_theme()


def draw_line_chart(data_frame: pd.DataFrame, timestamp_column_name: str, value_column_name: str,
    value_label: str, title: str):
    sampling_limit = 10000
    sampled_data_frame: pd.DataFrame = (data_frame.iloc[::round(data_frame.size / sampling_limit), :]
                                        if data_frame.size > sampling_limit else
                                        data_frame)

    formatted_data_frame = pd.DataFrame({
        'Date Time': (dt.datetime.utcfromtimestamp(timestamp / 1000)
                      for timestamp in sampled_data_frame[timestamp_column_name]),
        value_label: sampled_data_frame[value_column_name],
    })

    plot = sns.lineplot(data=formatted_data_frame, x='Date Time', y=value_label, linewidth=1.0)
    plot.set(title=f"{title} (sampled to max {sampling_limit} points)")
    plot.set_xticklabels(plot.get_xticklabels(), rotation=60)
