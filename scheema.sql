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