import datetime as dt

import pandas as pd
import seaborn as sns

sns.set_theme()


def draw_line_chart(timestamps: [int], values: [float], name: str):
    plot = sns.lineplot(data=pd.DataFrame({
        'Time': (dt.datetime.utcfromtimestamp(timestamp / 1000) for timestamp in timestamps),
        name: values,
    }), x='Time', y=name, linewidth=1.0)

    plot.set_xticklabels(plot.get_xticklabels(), rotation=60)
