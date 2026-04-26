import matplotlib.pyplot as plt

from task_4_oop_applications.base_classes import BaseVisualizer
from task_4_oop_applications.decorators import log_execution


class HorizontalBarVisualizer(BaseVisualizer):

    def __init__(
        self,
        output_path="current_chart.png",
        title="Top regions",
        xlabel="Number of vehicles",
        ylabel="Region",
        color="skyblue",
    ):
        super().__init__(output_path)
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.color = color

    @log_execution("Rendering horizontal bar chart")
    def render(self, data):

        if data is None or data.empty:
            raise ValueError("Cannot render an empty DataFrame.")

        category_col = data.columns[0]
        value_col = data.columns[1]

        plt.figure(figsize=(12, 8))
        plt.barh(data[category_col], data[value_col], color=self.color)
        plt.xlabel(self.xlabel, fontsize=12)
        plt.ylabel(self.ylabel, fontsize=12)
        plt.title(self.title, fontsize=14, fontweight="bold")
        plt.gca().invert_yaxis()
        plt.grid(axis="x", linestyle="--")
        plt.tight_layout()
        plt.savefig(self.output_path)
        plt.close()
        return self.output_path


class VerticalBarVisualizer(BaseVisualizer):

    def __init__(
        self,
        output_path="current_chart.png",
        title="Top regions",
        xlabel="Region",
        ylabel="Number of vehicles",
        color="steelblue",
    ):
        super().__init__(output_path)
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.color = color

    @log_execution("Rendering vertical bar chart")
    def render(self, data):
        if data is None or data.empty:
            raise ValueError("Cannot render an empty DataFrame.")

        category_col = data.columns[0]
        value_col = data.columns[1]

        plt.figure(figsize=(12, 8))
        plt.bar(data[category_col], data[value_col], color=self.color)
        plt.xlabel(self.xlabel, fontsize=12)
        plt.ylabel(self.ylabel, fontsize=12)
        plt.title(self.title, fontsize=14, fontweight="bold")
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis="y", linestyle="--")
        plt.tight_layout()
        plt.savefig(self.output_path)
        plt.close()
        return self.output_path