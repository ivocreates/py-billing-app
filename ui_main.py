from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Billing Application")
        MainWindow.setGeometry(100, 100, 1000, 600)
        MainWindow.setStyleSheet("""
            QWidget {
                background-color: #F5F7FA;
                color: #112D4E;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
        """)

        self.central_widget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Hidden bill ID field
        self.bill_id = QLineEdit()
        self.bill_id.setVisible(False)
        main_layout.addWidget(self.bill_id)

        # Customer Info Section
        customer_layout = QHBoxLayout()
        customer_layout.setSpacing(10)
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        self.name_input.setPlaceholderText("Full Name")
        self.phone_input.setPlaceholderText("Phone Number")
        self.email_input.setPlaceholderText("Email Address")

        for widget in [self.name_input, self.phone_input, self.email_input]:
            widget.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    border: 2px solid #DBE2EF;
                    border-radius: 12px;
                    background-color: white;
                }
                QLineEdit:focus {
                    border-color: #3F72AF;
                    background-color: #F0F4FA;
                }
            """)
            customer_layout.addWidget(widget)

        main_layout.addLayout(customer_layout)

        # Total Price Label
        self.total_label = QLabel("Total: ₹0.00")
        self.total_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.total_label.setAlignment(Qt.AlignRight)
        self.total_label.setStyleSheet("margin: 10px 0;")
        main_layout.addWidget(self.total_label)

        # Items Table Section
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Item", "Qty", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #DBE2EF;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #DBE2EF;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """)
        main_layout.addWidget(self.table, stretch=2)

        # Row Buttons
        row_btn_layout = QHBoxLayout()
        self.add_row_btn = QPushButton("➕ Add Row")
        self.remove_row_btn = QPushButton("➖ Remove Row")
        self.calculate_btn = QPushButton("Calculate Total")
        self.style_button(self.add_row_btn)
        self.style_button(self.remove_row_btn)
        self.style_button(self.calculate_btn)
        row_btn_layout.addWidget(self.add_row_btn)
        row_btn_layout.addWidget(self.remove_row_btn)
        row_btn_layout.addWidget(self.calculate_btn)
        row_btn_layout.addStretch()
        main_layout.addLayout(row_btn_layout)

        # Action Buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)
        self.new_btn = QPushButton("🆕 New")
        self.save_btn = QPushButton("💾 Save Bill")
        self.view_btn = QPushButton("📋 View Bills")
        self.export_btn = QPushButton("📤 Export PDF")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search by name/phone")

        for btn in [self.new_btn, self.save_btn, self.view_btn, self.export_btn]:
            self.style_button(btn)

        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #DBE2EF;
                border-radius: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3F72AF;
                background-color: #F0F4FA;
            }
        """)

        for widget in [self.new_btn, self.save_btn, self.view_btn, self.export_btn, self.search_input]:
            action_layout.addWidget(widget)

        main_layout.addLayout(action_layout)

        # Dashboard Summary
        dashboard_layout = QHBoxLayout()
        dashboard_layout.setSpacing(30)
        self.label_total_bills = QLabel("Total Bills: 0")
        self.label_revenue = QLabel("Revenue: ₹0.00")
        for label in [self.label_total_bills, self.label_revenue]:
            label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            label.setStyleSheet("padding: 10px;")
            dashboard_layout.addWidget(label)

        dashboard_layout.addStretch()
        main_layout.addLayout(dashboard_layout)

    def style_button(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #3F72AF;
                color: white;
                border-radius: 20px;
                padding: 10px 18px;
                font-weight: 600;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background-color: #365f91;
            }
        """)


# Main Window with logic
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect the New button
        self.ui.new_btn.clicked.connect(self.reset_new_bill)

    def reset_new_bill(self):
        # Clear inputs
        self.ui.name_input.clear()
        self.ui.phone_input.clear()
        self.ui.email_input.clear()
        self.ui.bill_id.clear()

        # Reset table properly
        self.ui.table.clear()
        self.ui.table.setRowCount(0)
        self.ui.table.setColumnCount(3)
        self.ui.table.setHorizontalHeaderLabels(["Item", "Qty", "Price"])

        # Reset total label
        self.ui.total_label.setText("Total: ₹0.00")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
