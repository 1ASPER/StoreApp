create_stores_query = """
CREATE TABLE IF NOT EXISTS stores 
(
    store_id        INTEGER PRIMARY KEY,
    name            TEXT,
    address         TEXT,
    working_time    TEXT
)
"""

create_products_query = """
CREATE TABLE IF NOT EXISTS products 
(
    product_id      INTEGER PRIMARY KEY,
    name            TEXT, 
    price           INTEGER
)
"""

create_sales_query = """
CREATE TABLE IF NOT EXISTS sales
(
    sale_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    date            TEXT,
    product_id      INTEGER,
    store_id        INTEGER,
    quantity        INTEGER,    

    FOREIGN KEY  (product_id)  REFERENCES  products (product_id),
    FOREIGN KEY  (store_id)    REFERENCES  stores   (store_id)
)
"""

insert_stores_query = "INSERT INTO stores VALUES (?, ?, ?)"
insert_products_query = "INSERT INTO products VALUES (?, ?, ?, ?)"
insert_sales_query = "INSERT INTO sales VALUES (?, ?, ?, ?, ?)"

selectmany_query = """
    SELECT sales.date, stores.name AS store_name, sales.quantity, products.price 
    FROM sales
    JOIN stores   ON sales.store_id   = stores.store_id
    JOIN products ON sales.product_id = products.product_id
    WHERE 1=1
"""