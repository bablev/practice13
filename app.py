from datetime import datetime

from flask import Flask, render_template, abort, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap
import sqlite3

app = Flask(__name__)
app.debug = True
bootstrap = Bootstrap(app)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/<int:invoiceId>')
def items(invoiceId):
    items = get_items(invoiceId)
    return render_template('item.html', items=items)


def get_items(invoice_id):
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM Item WHERE Invoiceid = ?',
                         (invoice_id,)).fetchall()
    conn.close()
    if items is None:
        abort(404)
    return items


@app.route('/create', methods=('GET', 'POST'))
def create():
    time = datetime.now().date()
    if request.method == 'POST':
        title = request.form['consignee']
        print(title)

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO  Invoice (consignee, created) VALUES (?, ?)',
                         (title, time))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM Invoice').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)
