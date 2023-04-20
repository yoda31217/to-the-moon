import datetime as dt

import matplotlib.dates as dates
import matplotlib.pyplot as plt


def draw_line_chart(timestamps: [int], values: [float], color: str = '#4caf50'):
    date_times = [dt.datetime.utcfromtimestamp(timestampSeconds / 1000) for timestampSeconds in timestamps]

    figure = plt.figure()
    axes = figure.add_subplot()
    axes.xaxis.set_major_formatter(dates.DateFormatter('%y-%m-%d %H:%M:%S'))
    plt.xticks(rotation=60)
    plt.grid(color='#bdbdbd', linestyle='--', linewidth=0.5)
    axes.plot(date_times, values, color, linewidth=1)
