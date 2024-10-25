import pandas as pd
import sqlite3
from sql_queries import *
from config import Config

connection = sqlite3.connect(Config.SQL_DATABASE_FILE_DIR, check_same_thread=False)
cursor = connection.cursor()

# Creating the tables
def create_tables(cursor: sqlite3.Cursor) -> None:
    """
    Creating an SQLite database with three tables:
    
    stores: Table to store information about different stores.
    - store_id (Primary Key)
    - name
    - address
    - working_time

    products: Table to store product information.
    - product_id (Primary Key)
    - name
    - price

    sales: Table to store transaction information. 
    - sale_id (Primary Key, Auto-increment)
    - date
    - product_id (Foreign Key from products)
    - store_id (Foreign Key from stores)
    - quantity


    Parameters:
        cursor (Cursor): The SQLite cursor object.

    """
    cursor.execute(create_stores_query)
    cursor.execute(create_products_query)
    cursor.execute(create_sales_query)


try:
    create_tables(cursor=cursor)
    print("Success!")

except sqlite3.Error as se:
    print("Something wrong in SQL queries\n", se)
    connection.rollback()
    connection.close()
    raise

except Exception as e:
    print("Something wrong\n", e)
    connection.rollback()
    connection.close()
    raise


# Loading data
try:
    for file_name in Config.CSV_FILE_NAMES:
        file_path = Config.PATH_TO_CSV_DIR + file_name

        df = pd.read_csv(file_path, sep=',')

        # Column name handler
        match file_name:
            case "products.csv":
                df.rename(columns={'id': 'product_id'}, inplace=True)
                df.rename(columns={'product': 'name'}, inplace=True)
            case "stores.csv":
                df.rename(columns={'id': 'store_id'}, inplace=True)

        table_name = file_name[:-4] # Removing "csv" extension from file name
        df.to_sql(table_name, connection, if_exists='append', index=False)

        print(f"{file_name} was added successfully")

except Exception as e:
    print("Something wrong\n", e)
    connection.rollback()
    connection.close()
    raise

connection.close()