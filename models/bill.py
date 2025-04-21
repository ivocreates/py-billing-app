import mysql.connector


class BillModel:
    def __init__(self, conn):
        self.conn = conn
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                items TEXT,
                total FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def add_bill(self, customer_id, items, total):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO bills (customer_id, items, total)
            VALUES (%s, %s, %s)
        """, (customer_id, items, total))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_bills(self):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT bills.*, customers.name, customers.phone
            FROM bills
            JOIN customers ON bills.customer_id = customers.id
            ORDER BY bills.created_at DESC
        """)
        return cursor.fetchall()
