import matplotlib.pyplot as plt

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
