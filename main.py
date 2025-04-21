import sys
import re
import json
import datetime

from functools import partial
from fpdf import FPDF

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog, QVBoxLayout,
    QTableWidgetItem, QLineEdit, QTableWidget, QPushButton, QStyledItemDelegate,
    QLabel, QSizePolicy, QHeaderView
)
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtCore import Qt

from db import DBHandler
from ui_main import Ui_MainWindow

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'


class NumericDelegate(QStyledItemDelegate):
    """Allows only integers for quantity and floats for price in the table."""
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        if index.column() == 1:
            editor.setValidator(QIntValidator(1, 9999, parent))
        elif index.column() == 2:
            validator = QDoubleValidator(0.0, 999999.99, 2, parent)
            validator.setNotation(QDoubleValidator.StandardNotation)
            editor.setValidator(validator)
        return editor


class EditItemDialog(QDialog):
    """Dialog to allow users to edit bill items."""
    def __init__(self, bill, db_handler):
        super().__init__()
        self.setWindowTitle("Edit Bill Items")
        self.bill = bill
        self.db_handler = db_handler

        self.layout = QVBoxLayout(self)
        self.table = QTableWidget(len(bill['items']), 3)
        self.table.setHorizontalHeaderLabels(['Item Name', 'Quantity', 'Price'])
        self.table.setItemDelegate(NumericDelegate(self.table))

        for i, (item, qty, price) in enumerate(bill['items']):
            self.table.setItem(i, 0, QTableWidgetItem(item))
            self.table.setItem(i, 1, QTableWidgetItem(str(qty)))
            self.table.setItem(i, 2, QTableWidgetItem(f"{price:.2f}"))

        self.layout.addWidget(self.table)

        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_button)

    def save_changes(self):
        updated_items = []
        for row in range(self.table.rowCount()):
            try:
                name = self.table.item(row, 0).text().strip()
                qty = int(self.table.item(row, 1).text())
                price = float(self.table.item(row, 2).text())
                if not name:
                    raise ValueError("Item name is empty")
                updated_items.append((name, qty, price))
            except Exception as e:
                QMessageBox.warning(self, "Invalid Data", f"Error at row {row + 1}: {e}")
                return

        try:
            total = sum(q * p for _, q, p in updated_items)
            self.db_handler.update_bill(self.bill['id'], json.dumps(updated_items), total)
            self.bill['items'] = updated_items
            self.bill['total'] = total
            QMessageBox.information(self, "Updated", "Bill updated successfully.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to update: {e}")


class BillingApp(QMainWindow):
    """Main billing application window."""
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = DBHandler()
        self.bills = []

        self.connect_signals()
        self.setup_ui()

    def setup_ui(self):
        self.ui.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.table.horizontalHeader().setStretchLastSection(True)
        self.ui.table.setItemDelegate(NumericDelegate())
        self.ui.table.setColumnCount(3)
        self.ui.table.setHorizontalHeaderLabels(["Item", "Quantity", "Price"])
        self.ui.table.setEditTriggers(QTableWidget.AllEditTriggers)

        self.ui.label_total_bills.setText("Total Bills: 0")
        self.ui.label_revenue.setText("Revenue: Rs.0.00")
        self.ui.total_label.setText("Total: Rs.0.00")

        footer_label = QLabel()
        footer_label.setTextFormat(Qt.RichText)
        footer_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        footer_label.setOpenExternalLinks(True)
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: gray; font-size: 12px; padding: 10px 0 0 0;")
        footer_label.setText(
            '🔗 <a href="https://github.com/ivocreates">GitHub</a> &nbsp;&nbsp; '
            '🌐 <a href="https://ivocreates.site">Portfolio</a> &nbsp;&nbsp; '
            '💼 <a href="https://linkedin.com/in/pereira-ivo">LinkedIn</a> <br>Created by Ivo Pereira'
        )

        layout = self.centralWidget().layout()
        if not layout:
            layout = QVBoxLayout(self.centralWidget())
        layout.addStretch()
        layout.addWidget(footer_label)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 5)

    def connect_signals(self):
        self.ui.add_row_btn.clicked.connect(self.add_row)
        self.ui.remove_row_btn.clicked.connect(self.remove_row)
        self.ui.calculate_btn.clicked.connect(self.calculate_total)
        self.ui.save_btn.clicked.connect(self.save_bill)
        self.ui.view_btn.clicked.connect(self.load_bills)
        self.ui.export_btn.clicked.connect(self.export_pdf)
        self.ui.search_input.textChanged.connect(self.search_bills)
        self.ui.new_btn.clicked.connect(self.clear_form)
        self.ui.table.itemChanged.connect(self.calculate_total)

    def add_row(self):
        self.ui.table.insertRow(self.ui.table.rowCount())

    def remove_row(self):
        row = self.ui.table.currentRow()
        if row != -1:
            self.ui.table.blockSignals(True)
            self.ui.table.removeRow(row)
            self.ui.table.blockSignals(False)
            self.calculate_total()

    def clear_form(self):
        self.ui.name_input.clear()
        self.ui.phone_input.clear()
        self.ui.email_input.clear()

        self.ui.table.setColumnCount(3)
        self.ui.table.setHorizontalHeaderLabels(["Item", "Quantity", "Price"])
        self.ui.table.setItemDelegate(NumericDelegate(self.ui.table))  # Reset delegate
        self.ui.table.setEditTriggers(QTableWidget.AllEditTriggers)
        self.ui.table.setRowCount(0)

        self.ui.total_label.setText("Total: Rs.0.00")


    def calculate_total(self):
        total = 0
        for row in range(self.ui.table.rowCount()):
            try:
                qty = int(self.ui.table.item(row, 1).text())
                price = float(self.ui.table.item(row, 2).text())
                total += qty * price
            except:
                continue
        self.ui.total_label.setText(f"Total: Rs.{total:.2f}")
        return total

    def save_bill(self):
        name = self.ui.name_input.text().strip()
        phone = self.ui.phone_input.text().strip()
        email = self.ui.email_input.text().strip()

        if not name or not phone:
            QMessageBox.warning(self, "Missing Info", "Name and phone are required.")
            return

        if email and not re.match(EMAIL_REGEX, email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return

        items = []
        for row in range(self.ui.table.rowCount()):
            try:
                item = self.ui.table.item(row, 0).text()
                qty = int(self.ui.table.item(row, 1).text())
                price = float(self.ui.table.item(row, 2).text())
                items.append((item, qty, price))
            except Exception:
                QMessageBox.warning(self, "Invalid Row", f"Check inputs at row {row + 1}")
                return

        if not items:
            QMessageBox.warning(self, "Empty Bill", "Add at least one item.")
            return

        total = sum(q * p for _, q, p in items)
        self.ui.total_label.setText(f"Total: Rs.{total:.2f}")

        try:
            customer_id = self.db.add_customer(name, email, phone)
            bill_id = self.db.add_bill(customer_id, json.dumps(items), total)
        except Exception as e:
            QMessageBox.critical(self, "DB Error", str(e))
            return

        new_bill = {
            "id": bill_id,
            "name": name,
            "phone": phone,
            "email": email,
            "items": items,
            "total": total,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.bills.append(new_bill)
        self.update_dashboard()
        self.clear_form()
        QMessageBox.information(self, "Saved", "Bill saved successfully!")

    def update_dashboard(self):
        self.ui.label_total_bills.setText(f"Total Bills: {len(self.bills)}")
        revenue = sum(b['total'] for b in self.bills)
        self.ui.label_revenue.setText(f"Revenue: Rs.{revenue:.2f}")

    def load_bills(self):
        self.ui.table.setRowCount(0)
        self.ui.table.setColumnCount(4)
        self.ui.table.setHorizontalHeaderLabels(["Customer", "Amount", "Date", "Action"])

        for bill in self.bills:
            row = self.ui.table.rowCount()
            self.ui.table.insertRow(row)
            self.ui.table.setItem(row, 0, QTableWidgetItem(bill["name"]))
            self.ui.table.setItem(row, 1, QTableWidgetItem(f"Rs.{bill['total']:.2f}"))
            self.ui.table.setItem(row, 2, QTableWidgetItem(bill["date"]))
            view_btn = QPushButton("View")
            view_btn.clicked.connect(lambda _, b=bill: self.view_bill(b))
            self.ui.table.setCellWidget(row, 3, view_btn)

    def print_bill(self, bill):
        file_path, _ = QFileDialog.getSaveFileName(self, "Print Bill", f"{bill['name']}_bill.pdf", "PDF files (*.pdf)")
        if not file_path:
            return

        pdf = FPDF()

        # Add a page and use a default font (e.g., Arial)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
    
        pdf.cell(200, 10, "Customer Bill", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.ln(5)

        pdf.cell(200, 10, f"Name: {bill['name']}", ln=True)
        pdf.cell(200, 10, f"Phone: {bill['phone']}", ln=True)
        pdf.cell(200, 10, f"Email: {bill['email']}", ln=True)
        pdf.cell(200, 10, f"Date: {bill['date']}", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(80, 10, "Item", border=1)
        pdf.cell(40, 10, "Quantity", border=1)
        pdf.cell(40, 10, "Price", border=1, ln=True)
        pdf.set_font("Arial", "", 12)

        for item, qty, price in bill['items']:
            pdf.cell(80, 10, item, border=1)
            pdf.cell(40, 10, str(qty), border=1)
            pdf.cell(40, 10, f"Rs.{price:.2f}", border=1, ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, f"Total: Rs.{bill['total']:.2f}", ln=True)

        try:
            pdf.output(file_path)
            QMessageBox.information(self, "Printed", f"Bill saved to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Print Failed", str(e))


    def search_bills(self, text):
        keyword = text.strip().lower()
        filtered = [b for b in self.bills if keyword in b["name"].lower() or keyword in b["phone"] or any(keyword in i[0].lower() for i in b["items"])]

        self.ui.table.setRowCount(0)
        for bill in filtered:
            row = self.ui.table.rowCount()
            self.ui.table.insertRow(row)
            self.ui.table.setItem(row, 0, QTableWidgetItem(bill["name"]))
            self.ui.table.setItem(row, 1, QTableWidgetItem(f"Rs.{bill['total']:.2f}"))
            self.ui.table.setItem(row, 2, QTableWidgetItem(bill["date"]))
            view_btn = QPushButton("View")
            view_btn.clicked.connect(lambda _, b=bill: self.view_bill(b))
            self.ui.table.setCellWidget(row, 3, view_btn)

    def view_bill(self, bill):
        detail = f"Name: {bill['name']}\nPhone: {bill['phone']}\nEmail: {bill['email']}\nDate: {bill['date']}\nTotal: Rs.{bill['total']:.2f}\n\nItems:\n"
        for item, qty, price in bill['items']:
            detail += f"{item} - Qty: {qty}, Price: Rs.{price:.2f}\n"

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Bill Details")
        msg_box.setText(detail)

        edit_btn = msg_box.addButton("Edit", QMessageBox.AcceptRole)
        delete_btn = msg_box.addButton("Delete", QMessageBox.DestructiveRole)
        print_btn = msg_box.addButton("Print", QMessageBox.ActionRole)
        msg_box.addButton("Close", QMessageBox.RejectRole)

        msg_box.exec()

        clicked = msg_box.clickedButton()
        if clicked == edit_btn:
            dialog = EditItemDialog(bill, self.db)
            if dialog.exec():
                self.update_dashboard()
                self.load_bills()
        elif clicked == delete_btn:
            self.delete_bill(bill)
        elif clicked == print_btn:
            self.print_bill(bill)

    def delete_bill(self, bill):
        try:
            self.db.delete_bill(bill['id'])
            self.bills.remove(bill)
            self.update_dashboard()
            self.load_bills()
            QMessageBox.information(self, "Deleted", "Bill deleted successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Delete Failed", str(e))

    def export_pdf(self):
        if not self.bills:
            QMessageBox.warning(self, "No Bills", "There are no bills to export.")
            return

    # Ask the user for the file path to save the PDF
        file_path, _ = QFileDialog.getSaveFileName(self, "Export All Bills", "all_bills.pdf", "PDF files (*.pdf)")
        if not file_path:
            return  # User canceled the dialog, exit early.

        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Use a default font (e.g., Arial)
            pdf.set_font("Arial", "", 12)
        
            pdf.cell(200, 10, "All Bills Summary", ln=True, align="C")
            pdf.ln(10)

            # Header for the bills list
            pdf.set_font("Arial", "B", 12)
            pdf.cell(50, 10, "Customer", border=1)
            pdf.cell(50, 10, "Amount", border=1)
            pdf.cell(50, 10, "Date", border=1)
            pdf.cell(40, 10, "Action", border=1, ln=True)
        
            pdf.set_font("Arial", "", 12)

            # Loop through the bills and write them into the PDF
            for bill in self.bills:
                pdf.cell(50, 10, bill["name"], border=1)
                pdf.cell(50, 10, f"Rs.{bill['total']:.2f}", border=1)  # Use Rs. directly
                pdf.cell(50, 10, bill["date"], border=1)
                pdf.cell(40, 10, "View", border=1, ln=True)  # Action column with a placeholder text

            pdf.ln(10)
            pdf.set_font("Arial", "B", 12)
            total_revenue = sum(bill["total"] for bill in self.bills)
            pdf.cell(200, 10, f"Total Revenue: Rs.{total_revenue:.2f}", ln=True, align="C")

            # Try saving the PDF to the specified file path
            pdf.output(file_path)
            QMessageBox.information(self, "Exported", f"All bills exported successfully to:\n{file_path}")
    
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"An error occurred while exporting the PDF:\n{str(e)}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingApp()
    window.show()
    sys.exit(app.exec())
