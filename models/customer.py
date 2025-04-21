import mysql.connector


class CustomerModel:
    def __init__(self, conn):
        self.conn = conn
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                phone VARCHAR(15) NOT NULL
            )
        """)
        self.conn.commit()

    def add_customer(self, name, email, phone):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO customers (name, email, phone)
            VALUES (%s, %s, %s)
        """, (name, email, phone))
        self.conn.commit()
        return cursor.lastrowid

    def get_customer_by_phone(self, phone):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE phone = %s", (phone,))
        return cursor.fetchone()
