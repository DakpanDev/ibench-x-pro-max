import matplotlib.pyplot as plt
import numpy as np

class LinePlot:
    def __init__(self, x_axis: list, y_axis: list, x_label: str, y_label: str, title: str):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.x_label = x_label
        self.y_label = y_label
        self.title = title

def plot_against_time(plots: list[LinePlot], title: str):
    start = min([int(np.floor(min(plot.x_axis))) for plot in plots])
    end = max([int(np.ceil(max(plot.x_axis))) for plot in plots])

    for plot in plots:
        plt.plot(plot.x_axis, plot.y_axis, markersize=2, label=plot.title)
    plt.xticks(np.arange(start, end + 1, 2))
    plt.xlabel('Time (s)')
    plt.ylabel(plots[0].y_label)
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()

class BoxPlot:
    def __init__(self, values: list, title: str):
        self.values = values
        self.title = title

def plot_regular_boxplot(plots: list[BoxPlot], y_label: str):
    values = [plot.values for plot in plots]
    labels = [plot.title for plot in plots]
    plt.boxplot(values, vert=True, patch_artist=True, labels=labels)
    plt.title(y_label)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
