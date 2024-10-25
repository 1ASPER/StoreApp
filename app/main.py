from flask import Flask
from flask import render_template
from .config import Config
import sqlite3

def create_app():

    app = Flask(__name__)
    
    def connect():
        conn = sqlite3.connect(Config.SQL_DATABASE_FILE_DIR, check_same_thread=False)
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
        

    return app