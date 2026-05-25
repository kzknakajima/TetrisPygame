from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'book-manager-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    status = db.Column(db.String(20), nullable=False, default='unread')
    rating = db.Column(db.Integer)
    memo = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_read = db.Column(db.DateTime)

    STATUS_LABELS = {
        'unread': '未読',
        'reading': '読書中',
        'read': '読了',
    }

    @property
    def status_label(self):
        return self.STATUS_LABELS.get(self.status, self.status)

    @property
    def stars(self):
        if self.rating is None:
            return ''
        return '★' * self.rating + '☆' * (5 - self.rating)


@app.route('/')
def index():
    query = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '')

    books_query = Book.query

    if query:
        books_query = books_query.filter(
            db.or_(
                Book.title.ilike(f'%{query}%'),
                Book.author.ilike(f'%{query}%'),
            )
        )

    if status_filter in ('unread', 'reading', 'read'):
        books_query = books_query.filter(Book.status == status_filter)

    books = books_query.order_by(Book.date_added.desc()).all()

    counts = {
        'all': Book.query.count(),
        'unread': Book.query.filter_by(status='unread').count(),
        'reading': Book.query.filter_by(status='reading').count(),
        'read': Book.query.filter_by(status='read').count(),
    }

    return render_template('index.html', books=books, counts=counts,
                           query=query, status_filter=status_filter)


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        genre = request.form.get('genre', '').strip()
        status = request.form.get('status', 'unread')
        rating_str = request.form.get('rating', '')
        memo = request.form.get('memo', '').strip()

        if not title or not author:
            flash('タイトルと著者は必須です。', 'error')
            return render_template('add_book.html')

        rating = int(rating_str) if rating_str.isdigit() and 1 <= int(rating_str) <= 5 else None
        date_read = datetime.utcnow() if status == 'read' else None

        book = Book(
            title=title,
            author=author,
            genre=genre or None,
            status=status,
            rating=rating,
            memo=memo or None,
            date_read=date_read,
        )
        db.session.add(book)
        db.session.commit()
        flash(f'「{title}」を登録しました。', 'success')
        return redirect(url_for('index'))

    return render_template('add_book.html')


@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        genre = request.form.get('genre', '').strip()
        status = request.form.get('status', 'unread')
        rating_str = request.form.get('rating', '')
        memo = request.form.get('memo', '').strip()

        if not title or not author:
            flash('タイトルと著者は必須です。', 'error')
            return render_template('edit_book.html', book=book)

        book.title = title
        book.author = author
        book.genre = genre or None
        book.status = status
        book.rating = int(rating_str) if rating_str.isdigit() and 1 <= int(rating_str) <= 5 else None
        book.memo = memo or None

        if status == 'read' and book.date_read is None:
            book.date_read = datetime.utcnow()
        elif status != 'read':
            book.date_read = None

        db.session.commit()
        flash(f'「{title}」を更新しました。', 'success')
        return redirect(url_for('index'))

    return render_template('edit_book.html', book=book)


@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    title = book.title
    db.session.delete(book)
    db.session.commit()
    flash(f'「{title}」を削除しました。', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
