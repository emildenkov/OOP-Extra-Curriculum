from abc import ABC, abstractmethod


class BaseAnalyzer(ABC):

    def __init__(self, file_path):
        self.file_path = file_path
        self._data_frame = None
        self._result = None


    @property
    def data_frame(self):
        return self._data_frame

    @data_frame.setter
    def data_frame(self, value):
        self._data_frame = value

    @property
    def result(self):
        return self._result

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def preprocess(self):
        pass

    @abstractmethod
    def analyze(self):
        pass

    def run(self, visualizer=None, report_builder=None):

        self.load_data()
        self.preprocess()
        self.analyze()

        chart_path = None
        if visualizer is not None:
            chart_path = visualizer.render(self._result)

        if report_builder is not None:
            report_builder.build(self._result, chart_path=chart_path)

        return self._result


class BaseVisualizer(ABC):

    def __init__(self, output_path="chart.png"):
        self.output_path = output_path

    @abstractmethod
    def render(self, data):
        pass


class BaseReportBuilder(ABC):

    def __init__(self, output_filename):
        self.output_filename = output_filename

    @abstractmethod
    def build(self, data, chart_path=None):
        pass