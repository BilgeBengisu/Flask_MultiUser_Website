from app import db, app
from models import Book

def add_books():
    with app.app_context():
        books = [
            Book(title="The Great Gatsby", author="F. Scott Fitzgerald", genre="Fiction", published_year=1925),
            Book(title="Moby-Dick", author="Herman Melville", genre="Adventure", published_year=1851),
            Book(title="Pride and Prejudice", author="Jane Austen", genre="Romance", published_year=1813),
        ]

        db.session.add_all(books)
        db.session.commit()
        print("Books added succesfully!")


if __name__ == "__main__":
    add_books()