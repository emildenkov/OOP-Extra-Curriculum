from task_4_oop_applications.vehicle_analyzer import VehicleDataAnalyzer
from task_4_oop_applications.visualizers import HorizontalBarVisualizer
from task_4_oop_applications.report_builders import VehiclePDFReportBuilder


def main():
    file_name = "task_2_pandas_and_visualization/" \
                "20-registrirani-pps-po-oblasti-i-vid-gorivo-pozitsiya-p3-v-srmps.csv"
    fuel_column = "БЕНЗИН-нови"

    analyzer = VehicleDataAnalyzer(
        file_path=file_name,
        fuel_column=fuel_column,
        top_n=10,
    )

    visualizer = HorizontalBarVisualizer(
        output_path="current_chart.png",
        title=f"Top 10 regions by registered vehicles ({fuel_column})",
        xlabel="Number of vehicles",
        ylabel="Region",
        color="skyblue",
    )

    report_builder = VehiclePDFReportBuilder(
        output_filename="Dynamic_Report.pdf",
        fuel_column=fuel_column,
    )

    try:
        analyzer.run(visualizer=visualizer, report_builder=report_builder)
        analyzer.display()

        print(f"\nTotal vehicles in top {analyzer.top_n}: "
              f"{analyzer.total_vehicles:.0f}")
        top_name, top_count = analyzer.top_region
        print(f"Leading region: {top_name} ({top_count:.0f} vehicles)")

    except Exception as exc:
        print(f"There was an error in the program: {exc}")


if __name__ == "__main__":
    main()