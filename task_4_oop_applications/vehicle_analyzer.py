import pandas as pd

from task_1_file_handling.universal_data_converter import UniversalDataConverter
from task_4_oop_applications.base_classes import BaseAnalyzer
from task_4_oop_applications.decorators import log_execution,timing,validate_dataframe


class VehicleDataAnalyzer(BaseAnalyzer):

    def __init__(self, file_path, fuel_column="БЕНЗИН-нови", top_n=10):
        super().__init__(file_path)
        self.fuel_column = fuel_column
        self.top_n = top_n
        self._region_column = None
        self._converter = None


    @property
    def region_column(self):
        return self._region_column

    @property
    def total_vehicles(self):
        if self._result is None:
            return None
        return self._result[self.fuel_column].sum()

    @property
    def top_region(self):
        if self._result is None or self._result.empty:
            return None
        row = self._result.iloc[0]
        return row[self._region_column], row[self.fuel_column]


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
                f"Available columns: {list(self._data_frame.columns)}"
            )

        self._data_frame[self.fuel_column] = pd.to_numeric(
            self._data_frame[self.fuel_column].astype(str).str.replace(" ", ""),
            errors="coerce",
        ).fillna(0)

        self._region_column = self._data_frame.columns[0]

    @log_execution("Analyzing")
    @timing
    @validate_dataframe
    def analyze(self):
        grouped = (
            self._data_frame
            .groupby(self._region_column)[self.fuel_column]
            .sum()
            .reset_index()
            .sort_values(by=self.fuel_column, ascending=False)
            .head(self.top_n)
        )
        self._result = grouped
        return grouped


    def display(self):
        if self._result is None:
            print("No result yet. Call run() or analyze() first.")
            return
        print("\n -- Top regions --")
        print(self._result.to_string(index=False))
        print("------------------\n")