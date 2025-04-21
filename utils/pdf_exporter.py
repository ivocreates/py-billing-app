from fpdf import FPDF
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class PDFExporter:
    @staticmethod
    def export_bill(bill, file_path):
        pdf = FPDF()
        pdf.add_page()

        # Add Unicode font (Ensure .ttf is present at this path)
        pdf.add_font("DejaVu", "", "assets/fonts/DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", "B", 16)
        pdf.cell(200, 10, txt="Customer Bill", ln=True, align="C")

        pdf.set_font("DejaVu", "", 12)
        pdf.cell(200, 10, txt=f"Name: {bill['name']}", ln=True)
        pdf.cell(200, 10, txt=f"Phone: {bill['phone']}", ln=True)
        pdf.cell(200, 10, txt=f"Email: {bill['email']}", ln=True)
        pdf.cell(200, 10, txt=f"Date: {bill['date']}", ln=True)

        pdf.ln(5)
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(60, 10, "Item", border=1)
        pdf.cell(40, 10, "Quantity", border=1)
        pdf.cell(40, 10, "Price", border=1)
        pdf.cell(40, 10, "Total", border=1)
        pdf.ln()

        pdf.set_font("DejaVu", "", 12)
        for item, qty, price in bill['items']:
            total = qty * price
            pdf.cell(60, 10, item, border=1)
            pdf.cell(40, 10, str(qty), border=1)
            pdf.cell(40, 10, f"{price:.2f}", border=1)
            pdf.cell(40, 10, f"{total:.2f}", border=1)
            pdf.ln()

        pdf.ln(5)
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(200, 10, txt=f"Total Amount: Rs. {bill['total']:.2f}", ln=True)

        # Output the PDF to file
        pdf.output(f"assets/{file_path}")