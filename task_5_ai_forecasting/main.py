import os.path

from task_5_ai_forecasting.forecast_analyzer import ForecastAnalyzer
from task_5_ai_forecasting.forecast_visualizers import ForecastLineVisualizer


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = os.path.join(project_root,
                             "task_2_pandas_and_visualization/",
                             "20-registrirani-pps-po-oblasti-i-vid-gorivo-pozitsiya-p3-v-srmps.csv")
    fuel_column = "БЕНЗИН-нови"

    analyzer = ForecastAnalyzer(
        file_path=file_name,
        fuel_column=fuel_column,
        forecast_steps=10,
        arima_order=(1, 1, 1),
    )

    visualizer = ForecastLineVisualizer(
        output_path="forecast_chart.png",
        title=f"ARIMA(1,1,1) forecast — vehicle registrations ({fuel_column})",
        history_color="steelblue",
        forecast_color="crimson",
        show_confidence=True,
    )

    try:
        analyzer.run()
        analyzer.display()

        payload = {
            "history": analyzer.series,
            "forecast": analyzer.forecast_mean,
            "ci_lower": analyzer.conf_int[:, 0],
            "ci_upper": analyzer.conf_int[:, 1],
            "label": fuel_column,
        }
        chart_path = visualizer.render(payload)

        print(f"Chart saved to: {chart_path}")
        print(f"Model AIC: {analyzer.aic:.2f}")
        print(f"Mean of forecast: {analyzer.forecast_mean.mean():.0f}")
        print(f"Historical mean : {analyzer.series.mean():.0f}")

    except Exception as exc:
        print(f"There was an error in the program: {exc}")


if __name__ == "__main__":
    main()