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
    conn = get_db_connection()
    status = conn.execute('SELECT Invoice.status FROM Invoice WHERE id = ?', (invoiceId,)).fetchone()[0]
    conn.close()
    return render_template('item.html', items=items, invoiceIdRequest=invoiceId, status=status)


def get_items(invoice_id):
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM Item WHERE Invoiceid = ?',
                         (invoice_id,)).fetchall()
    conn.close()
    if items is None:
        abort(404)
    return items


@app.route('/issued<int:invoiceId>', methods=['POST'])
def issuedInvoice(invoiceId):
    conn = get_db_connection()
    conn.execute('UPDATE Invoice SET status=? WHERE id = ?', ('Выдано', invoiceId))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/createItem<int:invoiceIdRequest>', methods=('GET', 'POST'))
def createItem(invoiceIdRequest):
    if request.method == 'POST':
        title = request.form['title']
        print(title)
        amount = int(request.form['amount'])
        print(amount)

        if not title:
            flash('Title is required')
        else:
            conn = get_db_connection()
            unit = conn.execute('SELECT Nomenclature.unit FROM Nomenclature WHERE title = ?', (title,)).fetchone()[0]
            print(unit)
            conn.execute('INSERT INTO Item(title,amount,unit,invoiceId) VALUES (?,?,?,?)',
                         (title, amount, unit, invoiceIdRequest))
            conn.commit()
            conn.close()
            return redirect(url_for('items', invoiceId=invoiceIdRequest))
    conn = get_db_connection()
    nomen = conn.execute('SELECT * FROM Nomenclature').fetchall()
    return render_template('createItem.html', nomen=nomen, invoiceId=invoiceIdRequest)


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
