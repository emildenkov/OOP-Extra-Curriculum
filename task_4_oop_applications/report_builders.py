from task_3_pdf_files.pdf_handling import PDFReportGenerator
from task_4_oop_applications.base_classes import BaseReportBuilder
from task_4_oop_applications.decorators import log_execution


class VehiclePDFReportBuilder(BaseReportBuilder):

    def __init__(self, output_filename="Dynamic_Report.pdf", fuel_column="БЕНЗИН-нови"):
        super().__init__(output_filename)
        self.fuel_column = fuel_column

    @log_execution("Building PDF report")
    def build(self, data, chart_path=None):

        if data is None or data.empty:
            raise ValueError("Cannot build a report from empty data.")

        region_col = data.columns[0]
        total_vehicles = data[self.fuel_column].sum()
        top_row = data.iloc[0]
        top_city = top_row[region_col]
        top_city_count = top_row[self.fuel_column]

        analysis_text = f"""
    Analyzing the registered vehicles ({self.fuel_column}):
    - Total number of vehicles: {total_vehicles:.0f}
    - Region with the highest number of registered vehicles: {top_city} ({top_city_count:.0f} vehicles)


    Summary:
    The data was successfully analyzed using the OOP pipeline.
    The chart below shows the distribution of registered vehicles
    across the leading regions.
    """

        report = PDFReportGenerator(self.output_filename)
        report.add_title("Automated Analysis Report")
        report.add_paragraph(analysis_text)
        if chart_path:
            report.add_image(chart_path, width=450, height=300)
        report.save_pdf()
        return self.output_filename