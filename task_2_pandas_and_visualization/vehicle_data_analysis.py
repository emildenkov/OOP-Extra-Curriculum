import pandas as pd
from task_1_file_handling.universal_data_converter import UniversalDataConverter
import matplotlib.pyplot as plt

from task_3_pdf_files.pdf_handling import generate_dynamic_report


def main():

    file_name = '20-registrirani-pps-po-oblasti-i-vid-gorivo-pozitsiya-p3-v-srmps.csv'

    try:

        converter = UniversalDataConverter(file_name)
        converter.read_file(delimiter=',', encoding='utf-8-sig')

        if converter.data_frame is None or len(converter.data_frame) <= 1:
            print('The standard settings are not working. We will try to recalibrate!')
            converter.read_file(delimiter=';', encoding='cd1251')

        if converter.data_frame is not None:
            df = converter.data_frame

            df.columns = df.columns.str.replace('"', '')

            targeted_col = 'БЕНЗИН-нови'

            df[targeted_col] = pd.to_numeric(df[targeted_col].astype(str).str.replace(' ', ''), errors='coerce').fillna(0)

            region_col = df.columns[0]

            grouped_df = df.groupby(region_col)[targeted_col].sum().reset_index()

            grouped_df = grouped_df.sort_values(by=[targeted_col], ascending=False).head(10)

            converter.container = grouped_df
            converter.display_data()

            plt.figure(figsize=(12, 8))

            plt.barh(grouped_df[region_col], grouped_df[targeted_col], color="skyblue")

            plt.xlabel("Number vehicles", fontsize=12)
            plt.ylabel('Region', fontsize=12)
            plt.title(f"Top 10 regions grouped by registered vehicles ({targeted_col})", fontsize=14, fontweight='bold')

            plt.gca().invert_yaxis()
            plt.grid(axis='x', linestyle='--')

            plt.tight_layout()

            chart_path = "current_chart.png"
            plt.savefig(chart_path)

            plt.show()

            total_cars = grouped_df[targeted_col].sum()
            best_city = grouped_df.iloc[0][region_col]
            best_count = grouped_df.iloc[0][targeted_col]

            generate_dynamic_report(
                total_vehicles=total_cars,
                top_city=best_city,
                top_city_count=best_count,
                chart_image_path=chart_path,
            )

    except Exception as e:
        print(f"There was an error in the program: {e}")


if __name__ == '__main__':
    main()