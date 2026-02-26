import os
import pandas as pd
from collections import namedtuple

class UniversalDataConverter:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data_frame = None
        self.container = None

    def read_file(self):

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file {self.file_path} doesn't exist")

        extension = os.path.splitext(self.file_path)[1].lower()

        try:
            if extension == ".csv":
                self.data_frame = pd.read_csv(self.file_path)
            elif extension == ".json":
                self.data_frame = pd.read_json(self.file_path)
            elif extension == ".xlsx":
                self.data_frame = pd.read_excel(self.file_path)
            elif extension == ".xml":
                self.data_frame = pd.read_xml(self.file_path)
            else:
                raise ValueError(f"Unsupported file format: {extension}")

            print(f"File {self.file_path} read successfully.")

        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            self.data_frame = None

    def create_container(self, container_type="list", element_type='dict'):

        if self.data_frame is None:
            return "No loaded data to convert."

        if container_type == "dataframe":
            self.container = self.data_frame

        if element_type == "dict":
            self.container = self.data_frame.to_dict('records')
        elif element_type == "namedtuple":
            DataPoint = namedtuple("DataPoint", self.container.columns)
            self.container = [DataPoint(*row) for row in self.data_frame.itertuples(index=False)]

        return self.container

    def display_data(self):
        if self.data_frame is not None:
            print(f'\n -- Visualization of the data --')
            print(self.container.to_string(index=False))
            print(f'---------------------------\n')
        else:
            print("No loaded data for visualizing.")

    def export_data(self, targeted_format):

        if self.data_frame is None:
            return "No loaded data to export."

        base_name = os.path.splitext(self.file_path)[0]
        output_name = f'{base_name}_converted.{targeted_format}'

        try:
            if targeted_format == '.csv':
                self.data_frame.to_csv(output_name, index=False)
            elif targeted_format == '.json':
                self.data_frame.to_json(output_name, orient='records', indent=4)
            elif targeted_format == '.xlsx':
                self.data_frame.to_excel(output_name, index=False)
            elif targeted_format == '.xml':
                self.data_frame.to_xml(output_name, index=False)
            else:
                return f"Unsupported file format: {targeted_format}"

            print(f"File {output_name} exported successfully.")

        except Exception as e:
            print(f"An error occurred while exporting the file: {e}")