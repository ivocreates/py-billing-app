<<<<<<< HEAD
# 💼 PySide python desktop application- Billing App 

A modern, full-featured desktop billing system built with **PySide6**, **MySQL**, and **FPDF**, designed for small businesses to manage customer billing, track sales, and generate invoices.

---

## 📌 Features

- 🧾 **Customer Billing Form** with real-time total calculation  
- 🗂️ **Grouped Bill Listing** under customer names  
- 🔍 **Live Search** across customers and bills  
- 📄 **Export to PDF** (single bill + all bill summary)  
- ✅ **Full CRUD** operations for customers and bills  
- 🖱️ responsive UI  
- 🔒 Data validation for numeric fields, phone numbers, emails, etc.  

---

## 🗂️ Project Structure

pyside_billing_app/ 
├── main.py # Main app logic
├── ui_main.py # UI of the application
├── db.py # MySQL database connection 
├── assets/ 
│ └── logo.png  
├── models/ 
│ ├── customer.py # Customer DB interaction logic 
│ └── bill.py # Bill DB interaction logic 
├── utils/ 
│ └── pdf_exporter.py # Bill PDF export logic using FPDF 
├── requirements.txt # Python dependencies 
└── README.md # Project documentation


---

## ⚙️ Setup Instructions

1. **Clone the repository**
git clone https://github.com/ivocreates/py-billing-app.git
cd pyside-billing-app
Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Set up the MySQL database

Login to MySQL and run:

CREATE DATABASE billing_app;

USE billing_app;

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);

CREATE TABLE bills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    item TEXT,
    quantity INT,
    price DECIMAL(10,2),
    total DECIMAL(10,2),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

Update DB credentials in db.py

# db.py
config = {
    'user': 'root',
    'password': 'yourpassword',
    'host': 'localhost',
    'database': 'billing_app'
}

Run the app

python main.py


💻 Tech Stack
Python 3.x

PySide6 – GUI Framework

MySQL – Database

mysql-connector-python – DB connector

FPDF – PDF generation


📁 File Descriptions

File/Folder	Description
main.py	Main app window and UI logic
db.py	Handles MySQL connection
models/customer.py	Customer DB operations
models/bill.py	Bill DB operations
utils/pdf_exporter.py	PDF generation for bills
assets/logo.png	App logo
requirements.txt	Python dependencies
README.md	Project documentation

🖼️ Screenshots
![Making Bills](<Screenshot 2025-04-19 113545.png>)
![Viewing Bills](<Screenshot 2025-04-19 124754.png>)

Demo- Video Explanation
https://drive.google.com/file/d/1ob11KtFCrGOlc4ePZC9-sdbZEWoZPZwP/view?usp=sharing


🧑‍💻 Author
Ivo Pereira
Web & Software Developer | Computer Science Student
🔗 GitHub: https://github.com/ivocreates
🌐 Portfolio: https://ivocreates.site
💼 LinkedIn: https://linkedin.com/in/pereira-ivo 


🤝 Contributing
Contributions are welcome!
Fork this repo, create a feature branch, and submit a pull request.

git checkout -b feature/your-feature
git commit -m "Add: Your feature"
git push origin feature/your-feature

📜 License
This project is open-source and available under the MIT License.

🧠 Future Enhancements
Role-based authentication (admin/user)

Bill emailing

Product inventory tracking

SQLite support for easy local use
=======
# py-billing-app
A modern, full-featured desktop billing system built with **PySide6**, **MySQL**, and **FPDF**, designed for small businesses to manage customer billing, track sales, and generate invoices.
>>>>>>> 8875d52f36737151efb4e720b8f9732015f51452
