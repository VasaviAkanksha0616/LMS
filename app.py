from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db
from models.book_model import Book
from models.member_model import Member
from models.transaction_model import Transaction
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    books_count = Book.query.count()
    members_count = Member.query.count()
    return render_template('dashboard.html', books=books_count, members=members_count)

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        db.session.add(Book(title=title, author=author))
        db.session.commit()
        return redirect(url_for('books'))
    return render_template('books.html', books=Book.query.all())

@app.route('/members', methods=['GET', 'POST'])
def members():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        db.session.add(Member(name=name, email=email))
        db.session.commit()
        return redirect(url_for('members'))
    return render_template('members.html', members=Member.query.all())

@app.route('/issue_return', methods=['GET', 'POST'])
def issue_return():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        member_id = int(request.form['member_id'])
        action = request.form['action']
        if action == 'issue':
            tx = Transaction(book_id=book_id, member_id=member_id)
            Book.query.get(book_id).status = 'issued'
            db.session.add(tx)
            db.session.commit()
        elif action == 'return':
            tx = Transaction.query.filter_by(book_id=book_id, member_id=member_id, return_date=None).first()
            if tx:
                days = (datetime.utcnow() - tx.issue_date).days
                fine = max(0, (days - 14) * 5)
                tx.return_date = datetime.utcnow()
                tx.fine = fine
                Book.query.get(book_id).status = 'available'
                db.session.commit()
        return redirect(url_for('issue_return'))
    return render_template('issue_return.html', books=Book.query.all(), members=Member.query.all())

@app.route('/reports')
def reports():
    return render_template('reports.html', transactions=Transaction.query.all())

@app.route('/request_book', methods=['GET', 'POST'])
def request_book():
    if request.method == 'POST':
        title = request.form['title']
        # Here you could send an email or save request to DB
        return f"Request submitted for: {title}"
    return render_template('request_book.html')

if __name__ == '__main__':
    app.run(debug=True)
