import warnings
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

from task_1_file_handling.universal_data_converter import UniversalDataConverter
from task_4_oop_applications.base_classes import BaseAnalyzer
from task_4_oop_applications.decorators import log_execution,timing,validate_dataframe


warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


class ForecastAnalyzer(BaseAnalyzer):

    _AGGREGATE_LABELS = {"ОБЩО", "OBSHTO", "TOTAL"}

    def __init__(
        self,
        file_path,
        fuel_column="БЕНЗИН-нови",
        forecast_steps=10,
        arima_order=(1, 1, 1),
        exclude_aggregates=True,
    ):
        super().__init__(file_path)
        self.fuel_column = fuel_column
        self.forecast_steps = forecast_steps
        self.arima_order = arima_order
        self.exclude_aggregates = exclude_aggregates

        self._region_column = None
        self._converter = None
        self._series = None
        self._forecast_mean = None
        self._conf_int = None
        self._fitted_model = None


    @property
    def series(self):
        return self._series

    @property
    def forecast_mean(self):
        return self._forecast_mean

    @property
    def conf_int(self):
        return self._conf_int

    @property
    def aic(self):
        if self._fitted_model is None:
            return None
        return self._fitted_model.aic

    @log_execution("Loading vehicle CSV")
    def load_data(self):
        self._converter = UniversalDataConverter(self.file_path)
        self._converter.read_file(delimiter=",", encoding="utf-8-sig")

        df = self._converter.data_frame
        if df is None or len(df) <= 1 or len(df.columns) <= 1:
            print("Default settings did not parse the file — recalibrating...")
            self._converter.read_file(delimiter=";", encoding="cp1251")
            df = self._converter.data_frame

        self._data_frame = df

    @log_execution("Preprocessing")
    @validate_dataframe
    def preprocess(self):
        self._data_frame.columns = self._data_frame.columns.str.replace('"', "")

        if self.fuel_column not in self._data_frame.columns:
            raise KeyError(
                f"Column '{self.fuel_column}' not found. "
                f"Available: {list(self._data_frame.columns)}"
            )

        self._data_frame[self.fuel_column] = pd.to_numeric(
            self._data_frame[self.fuel_column].astype(str).str.replace(" ", ""),
            errors="coerce",
        ).fillna(0)

        self._region_column = self._data_frame.columns[0]

        series = (
            self._data_frame
            .groupby(self._region_column)[self.fuel_column]
            .sum()
            .sort_index()
        )

        if self.exclude_aggregates:
            mask = ~series.index.str.upper().isin(self._AGGREGATE_LABELS)
            dropped = series.index[~mask].tolist()
            if dropped:
                print(f"Dropped aggregate row(s): {dropped}")
            series = series[mask]

        self._series = series
        print(f"Time series ready: {len(series)} points, "
              f"mean={series.mean():.0f}, std={series.std():.0f}")

    @log_execution("ARIMA forecast")
    @timing
    @validate_dataframe
    def analyze(self):
        if self._series is None or len(self._series) < 5:
            raise RuntimeError(
                "Series too short for ARIMA. Need at least ~5 points; "
                f"have {0 if self._series is None else len(self._series)}."
            )

        model = ARIMA(self._series.values, order=self.arima_order)
        self._fitted_model = model.fit()
        print(f"Fitted ARIMA{self.arima_order} — AIC: {self._fitted_model.aic:.2f}")

        forecast_result = self._fitted_model.get_forecast(steps=self.forecast_steps)
        self._forecast_mean = np.asarray(forecast_result.predicted_mean)
        self._conf_int = np.asarray(forecast_result.conf_int(alpha=0.05))

        self._result = pd.DataFrame({
            "step": range(1, self.forecast_steps + 1),
            "forecast": self._forecast_mean,
            "ci_lower": self._conf_int[:, 0],
            "ci_upper": self._conf_int[:, 1],
        })
        return self._result

    def display(self):
        if self._result is None:
            print("No result yet. Call run() or analyze() first.")
            return
        print("\n -- ARIMA forecast --")
        print(self._result.to_string(index=False, float_format=lambda x: f"{x:>9.1f}"))
        print("--------------------\n")