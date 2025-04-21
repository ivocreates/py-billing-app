import mysql.connector

class DBHandler:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="billing_db"
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self.init_db()

    def init_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                phone VARCHAR(15)
            )
        """)
        self.cursor.execute("""
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

    def add_customer(self, name, email, phone):
        self.cursor.execute(
            "SELECT id FROM customers WHERE name=%s AND phone=%s",
            (name, phone)
        )
        result = self.cursor.fetchone()
        if result:
            return result['id']
        self.cursor.execute(
            "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def add_bill(self, customer_id, items_json, total):
        self.cursor.execute(
            "INSERT INTO bills (customer_id, items, total) VALUES (%s, %s, %s)",
            (customer_id, items_json, total)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update_bill(self, bill_id, items_json, total):
        query = "UPDATE bills SET items=%s, total=%s WHERE id=%s"
        self.cursor.execute(query, (items_json, total, bill_id))
        self.conn.commit()

    def delete_bill(self, bill_id):
        self.cursor.execute("DELETE FROM bills WHERE id=%s", (bill_id,))
        self.conn.commit()

    def get_all_bills(self):
        self.cursor.execute("""
            SELECT b.id, c.name, c.phone, c.email, b.items, b.total, b.created_at AS date
            FROM bills b
            JOIN customers c ON b.customer_id = c.id
            ORDER BY b.created_at DESC
        """)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
