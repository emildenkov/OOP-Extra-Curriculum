import matplotlib.pyplot as plt

from task_4_oop_applications.base_classes import BaseVisualizer
from task_4_oop_applications.decorators import log_execution


class ForecastLineVisualizer(BaseVisualizer):

    def __init__(
        self,
        output_path="forecast_chart.png",
        title="Time-series forecast",
        history_color="steelblue",
        forecast_color="crimson",
        show_confidence=True,
    ):
        super().__init__(output_path)
        self.title = title
        self.history_color = history_color
        self.forecast_color = forecast_color
        self.show_confidence = show_confidence

    @log_execution("Rendering forecast line chart")
    def render(self, data):
        required = {"history", "forecast", "ci_lower", "ci_upper", "label"}
        missing = required - set(data.keys())
        if missing:
            raise ValueError(f"Missing keys in data payload: {missing}")

        history = data["history"]
        forecast = data["forecast"]
        ci_lower = data["ci_lower"]
        ci_upper = data["ci_upper"]
        label = data["label"]

        n_hist = len(history)
        n_fcst = len(forecast)
        hist_x = list(range(n_hist))
        forecast_x = list(range(n_hist, n_hist + n_fcst))

        fig, ax = plt.subplots(figsize=(14, 7))

        ax.plot(hist_x, history.values, marker="o", linewidth=2,
                color=self.history_color,
                label=f"Historical ({n_hist} points)")

        ax.plot([hist_x[-1], forecast_x[0]],
                [history.values[-1], forecast[0]],
                color="gray", linestyle="--", linewidth=1)

        ax.plot(forecast_x, forecast, marker="s", linewidth=2,
                color=self.forecast_color,
                label=f"Forecast ({n_fcst} points)")

        if self.show_confidence:
            ax.fill_between(
                forecast_x, ci_lower, ci_upper,
                color=self.forecast_color, alpha=0.15,
                label="95% confidence interval",
            )

        ax.axvline(x=n_hist - 0.5, color="black", linestyle=":", alpha=0.5)

        ax.set_xlabel("Region index (sorted alphabetically)", fontsize=12)
        ax.set_ylabel(f"Number of vehicles ({label})", fontsize=12)
        ax.set_title(self.title, fontsize=14, fontweight="bold")
        ax.legend(loc="upper right", fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.5)

        all_labels = list(history.index) + [f"Synth+{i+1}" for i in range(n_fcst)]
        ax.set_xticks(range(len(all_labels)))
        ax.set_xticklabels(all_labels, rotation=45, ha="right", fontsize=8)

        plt.tight_layout()
        plt.savefig(self.output_path, dpi=120)
        plt.close()

        return self.output_path