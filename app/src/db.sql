-- Create the User table
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE
    users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        balance DECIMAL(19, 4) NOT NULL DEFAULT 0
    );

-- Create the Product table
DROP TABLE IF EXISTS products CASCADE;

CREATE TABLE
    products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE,
        price DECIMAL(19, 4) NOT NULL
    );

-- Create the Junction table for User and Product with quantity
DROP TABLE IF EXISTS inventory CASCADE;

CREATE TABLE
    inventory (
        transaction_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users (user_id),
        product_id INT REFERENCES products (product_id),
        purchase_date DATE NOT NULL DEFAULT CURRENT_DATE
    );

INSERT INTO
    users (username, password, balance)
VALUES
    ('john_doe', 'password123',20),
    ('jane_smith', 'letmein',20),
    ('michael_jackson', 'thriller',0),
    ('maria_garcia', '123456',0),
    ('chris_evans', 'captainamerica',0),
    ('emma_watson', 'hermione',0),
    ('david_beckham', 'football',20),
    ('sid', '123',2000);

INSERT INTO
    products (name, price)
VALUES
    ('Bananas',5),
    ('Milk',10),
    ('Lego Set',150),
    ('Barbie',50),
    ('PlayStation 5', 500),
    ('iPhone 13 Pro', 1099.99),
    ('Samsung Galaxy S21', 899.99),
    ('Nintendo Switch', 299.99),
    ('MacBook Pro 13"', 1299.99),
    ('Dell XPS 15', 1399.99),
    ('Nike Air Max', 99.99),
    ('Adidas Ultraboost', 139.99);

INSERT INTO
    inventory (user_id, product_id)
VALUES
    (8, 3)
    -- (1, 1, 5),
    -- (1, 3, 2),
    -- (2, 2, 3),
    -- (2, 5, 1),
    -- (3, 4, 4),
    -- (3, 7, 2),
    -- (4, 8, 6),
    -- (5, 1, 1),
    -- (5, 3, 2),
    -- (6, 4, 2),
    -- (6, 6, 1),
    -- (7, 5, 4),
    -- (7, 7, 3),
    -- (8, 2, 2),
    -- (8, 8, 1),
    -- (5, 2, 1),
    -- (8, 1, 1),
    -- (4, 7, 4),
    -- (5, 8, 2),
    -- (7, 4, 2),
    -- (8, 6, 3);