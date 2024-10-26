from flask import Flask
from flask import render_template
from flask import request
from .config import Config
from sql_queries import selectmany_query
import sqlite3

def create_app() -> Flask.wsgi_app:

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

        store_filter = request.form.getlist('store_filter') or [stores[0][1]] if stores else []
        product_filter = request.form.getlist('product_filter') or [products[0][1]] if products else []
        start_date = request.form.get('start_date', None)
        end_date = request.form.get('end_date', None)

        query = selectmany_query
        
        params = []
        if store_filter:
            query += ' AND stores.name IN ({})'.format(','.join(['?'] * len(store_filter)))
            params.extend(store_filter)
        
        if product_filter:
            query += ' AND products.name IN ({})'.format(','.join(['?'] * len(product_filter)))
            params.extend(product_filter)
        
        if start_date and end_date:
            query += ' AND sales.date BETWEEN ? AND ?'
            params.extend([start_date, end_date])

        sales = conn.execute(query, params).fetchall()

        total_quantity = sum(int(sale[2]) for sale in sales)
        total_amount = sum(int(sale[2]) * int(sale[3]) for sale in sales)

        conn.close()

        return render_template( 'analytics.html',
            sales_data=sales,
            total_quantity=total_quantity,
            total_amount=total_amount,
            stores=stores,
            products=products,
            store_filter=store_filter,
            product_filter=product_filter
        )


    return app