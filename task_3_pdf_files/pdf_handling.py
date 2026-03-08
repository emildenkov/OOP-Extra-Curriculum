import os
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class PDFManipulator:

    @staticmethod
    def extract_text_from_pdf(pdf_path, page_num=0):
        try:
            reader = PdfReader(pdf_path)
            page = reader.pages[page_num]
            return page.extractText()

        except Exception as e:
            return f"Error extracting text: {e}"

    @staticmethod
    def merge_pdfs(pdf_list, output_path):
        merger = PdfMerger()

        try:
            for pdf in pdf_list:
                merger.append(pdf)
            merger.write(output_path)
            merger.close()
            return f"PDFs merged successfully into {output_path}"

        except Exception as e:
            return f"Error merging PDFs: {e}"

    @staticmethod
    def rotate_page(pdf_path, output_path, page_num=0, rotation=90):
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            for i, page in enumerate(reader.pages):
                if i == page_num:
                    page.rotate(rotation)
                writer.add_page(page)

            with open(output_path, "wb") as f:
                writer.write(f)
            print(f"Page {page_num} rotated successfully in {output_path}")

        except Exception as e:
            print(f"Error rotating page: {e}")


class PDFReportGenerator:

    def __init__(self, output_filename):
        self.output_filename = output_filename
        self.c = canvas.Canvas(self.output_filename, pagesize=A4)
        self.width, self.height = A4
        self.current_y = self.height - 50

    def add_title(self, title):
        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, self.current_y, title)
        self.current_y -= 40

    def add_paragraph(self, text):
        self.c.setFont("Helvetica", 12)

        for line in text.split('\n'):
            self.c.drawString(50, self.current_y, line)
            self.current_y -= 20
        self.current_y -= 10

    def add_image(self, image_path, width=400, height=300):
        if os.path.exists(image_path):
            if self.current_y - height < 50:
                self.c.showPage()
                self.current_y = self.height - 50

            self.c.drawImage(image_path, 50, self.current_y - height, width=width, height=height)
            self.current_y -= (height + 30)

        else:
            self.add_paragraph(f"[Missing image: {image_path}]")

    def save_pdf(self):
        self.c.save()
        print(f"PDF report saved as {self.output_filename}")


def generate_dynamic_report(total_vehicles, top_city, top_city_count, chart_image_path, report_name="Dynamic_Report.pdf"):

    print("\nGenerating dynamic report...")

    analysis_text = f"""
    Analyzing the registered vehicles:
    - Total number of vehicles: {total_vehicles:.0f}
    -Region with the highest number of registered vehicles: {top_city} ({top_city_count:.0f} vehicles)


    Summary:
    The data was successfully analyzed with Pandas.
    The graphic below shows the distribution of registered vehicles across the main regions.
    """

    report = PDFReportGenerator(report_name)
    report.add_title("Automated Analysis Report")
    report.add_paragraph(analysis_text)

    report.add_image(chart_image_path, width=450, height=300)
    report.save_pdf()