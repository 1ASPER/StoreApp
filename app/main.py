from flask import Flask
from flask import render_template
from flask import request
from .config import Config
import sqlite3

def create_app():

    app = Flask(__name__)
    
    def connect():
        conn = sqlite3.connect(Config.SQL_DATABASE_FILE_DIR, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    @app.route('/')
    def home():
        return render_template('home.html')
    

    @app.route('/stores')
    def stores():
        conn = connect()
        c = conn.cursor()
        data = c.execute('SELECT * FROM stores').fetchall()
        c.close()
        return render_template("stores.html", stores=data)
    

    @app.route('/products')
    def products():
        conn = connect()
        c = conn.cursor()
        data = c.execute('SELECT * FROM products').fetchall()
        c.close()

        return render_template("products.html", products=data)
    
    @app.route('/analytics', methods=['GET', 'POST'])
    def analytics():
        conn = connect()
        
        stores = conn.execute('SELECT * FROM stores').fetchall()
        products = conn.execute('SELECT * FROM products').fetchall()

        store_filter = request.form.get('store_filter', None)
        product_filter = request.form.get('product_filter', None)
        start_date = request.form.get('start_date', None)
        end_date = request.form.get('end_date', None)

        query = """
                SELECT  sales.date, stores.name AS store_name, sales.quantity, products.price FROM sales
                JOIN    stores      ON  sales.store_id   =  stores.store_id 
                JOIN    products    ON  sales.product_id =  products.product_id WHERE 1=1
                """
        
        params = []
        if store_filter:
            query += ' AND stores.name = ?'
            params.append(store_filter)
        
        if product_filter:
            query += ' AND products.name = ?'
            params.append(product_filter)
        
        if start_date and end_date:
            query += ' AND sales.date BETWEEN ? AND ?'
            params.extend([start_date, end_date])

        sales_data = conn.execute(query, params).fetchall()

        total_quantity = sum(int(sale[2]) for sale in sales_data)  # 2 - индекс quantity
        total_amount = sum(int(sale[2]) * float(sale[3]) for sale in sales_data)

        total_quantity = sum(sale['quantity'] for sale in sales_data)
        total_amount = sum(sale['quantity'] * sale['price'] for sale in sales_data)

        conn.close()
        
        return render_template('analytics.html', 
                            sales_data=sales_data,
                            total_quantity=total_quantity, 
                            total_amount=total_amount,
                            stores=stores, 
                            products=products)

        
    return app