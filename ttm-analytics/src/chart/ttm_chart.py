from datetime import datetime

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

sns.set_theme()


def draw_line_chart(data_frame: pd.DataFrame, timestamp_column_name: str, value_column_name: str,
                    value_label: str, title: str):
    sampling_limit = 100000
    sampled_data_frame: pd.DataFrame = (data_frame.iloc[::round(data_frame.size / sampling_limit), :]
                                        if data_frame.size > sampling_limit else
                                        data_frame)

    formatted_data_frame = pd.DataFrame({
        'Date Time': sampled_data_frame[timestamp_column_name],
        value_label: sampled_data_frame[value_column_name],
    })

    fig, ax = plt.subplots(figsize=(16, 9))
    plot = sns.lineplot(data=formatted_data_frame, x='Date Time', y=value_label, linewidth=1.0, ax=ax)

    min_timestamp = sampled_data_frame[timestamp_column_name].min()
    max_timestamp = sampled_data_frame[timestamp_column_name].max()
    plot_ticks_count = 40
    plot_x_ticks = [min_timestamp + round(i * (max_timestamp - min_timestamp) / float(plot_ticks_count))
                    for i in range(0, plot_ticks_count + 1)]
    plot.set_xticks(plot_x_ticks)
    plot.set_xticklabels([datetime.utcfromtimestamp(plot_x_tick / 1000).strftime("%m/%d %H:%M")
                          for plot_x_tick in plot_x_ticks])

    plot.set(title=f"{title} (sampled)")
    plot.set_xticklabels(plot.get_xticklabels(), rotation=90)
