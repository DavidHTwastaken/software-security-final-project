-- Create the User table
DROP TABLE IF EXISTS users;

CREATE TABLE
    users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL
    );

-- Create the Product table
DROP TABLE IF EXISTS products;

CREATE TABLE
    products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE,
        price DECIMAL(19, 4) NOT NULL
    );

-- Create the Junction table for User and Product with quantity
DROP TABLE IF EXISTS user_products;

CREATE TABLE
    user_products (
        user_id INT REFERENCES users (user_id),
        product_id INT REFERENCES products (product_id),
        quantity INT DEFAULT 0,
        PRIMARY KEY (user_id, product_id)
    );

INSERT INTO
    users (username, password)
VALUES
    ('john_doe', 'password123'),
    ('jane_smith', 'letmein'),
    ('michael_jackson', 'thriller'),
    ('maria_garcia', '123456'),
    ('chris_evans', 'captainamerica'),
    ('emma_watson', 'hermione'),
    ('david_beckham', 'football'),
    ('serena_williams', 'tennis');

INSERT INTO
    products (name, price)
VALUES
    ('iPhone 13 Pro', 1099.99),
    ('Samsung Galaxy S21', 899.99),
    ('PlayStation 5', 499.99),
    ('Nintendo Switch', 299.99),
    ('MacBook Pro 13"', 1299.99),
    ('Dell XPS 15', 1399.99),
    ('Nike Air Max', 99.99),
    ('Adidas Ultraboost', 139.99);

INSERT INTO
    user_products (user_id, product_id, quantity)
VALUES
    (1, 1, 5),
    (1, 3, 2),
    (2, 2, 3),
    (2, 5, 1),
    (3, 4, 4),
    (3, 7, 2),
    (4, 6, 3),
    (4, 8, 6),
    (5, 1, 1),
    (5, 3, 2),
    (6, 4, 2),
    (6, 6, 1),
    (7, 5, 4),
    (7, 7, 3),
    (8, 2, 2),
    (8, 8, 1),
    (1, 2, 2),
    (2, 1, 1),
    (3, 3, 3),
    (4, 5, 2),
    (5, 4, 1),
    (6, 7, 4),
    (7, 6, 2),
    (8, 3, 1),
    (1, 8, 3),
    (2, 4, 4),
    (3, 2, 1),
    (4, 1, 2),
    (5, 5, 3),
    (6, 8, 1),
    (7, 3, 2),
    (8, 7, 3),
    (1, 4, 1),
    (2, 3, 2),
    (3, 5, 3),
    (4, 6, 2),
    (5, 7, 1),
    (6, 1, 2),
    (7, 8, 4),
    (8, 4, 2),
    (1, 3, 1),
    (2, 5, 2),
    (3, 7, 3),
    (4, 8, 2),
    (5, 2, 1),
    (6, 4, 3),
    (7, 6, 2),
    (8, 1, 1),
    (1, 2, 2),
    (2, 3, 3),
    (3, 5, 1),
    (4, 7, 4),
    (5, 8, 2),
    (6, 1, 1),
    (7, 4, 2),
    (8, 6, 3);