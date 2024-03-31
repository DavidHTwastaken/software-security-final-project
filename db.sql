-- Create the User table
CREATE TABLE
    users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL
    );

-- Create the Product table
CREATE TABLE
    products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL
    );

-- Create the Junction table for User and Product with quantity
CREATE TABLE
    user_products (
        user_id INT REFERENCES users (user_id),
        product_id INT REFERENCES products (product_id),
        quantity INT,
        PRIMARY KEY (user_id, product_id)
    );