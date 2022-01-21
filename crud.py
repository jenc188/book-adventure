"""CRUD operations."""

from model import db, User, Book, Favorite, User_Rating, connect_to_db

def create_user(first_name, last_name, email, user_password):
    """Create and return a new user."""

    user = User(first_name=first_name, last_name=last_name,email=email, user_password=user_password)

    db.session.add(user)
    db.session.commit()

    return user

def get_user_by_email(email):
    """ Get user with email."""

    user = User.query.filter_by(email=email).first()

    return user



def create_book (book_title, author, isbn, num_page, language_code, avg_rating):
    """Create and return a new movie."""

    book = Book(
        book_title=book_title, 
        author=author,
        isbn=isbn,
        num_page=num_page,
        language_code=language_code,
        avg_rating=avg_rating
        )

    db.session.add(book)
    db.session.commit()

    return book

def get_all_books():
    """Return list of all books(Book objects)"""
    
    books = Book.query.all()

    return books

def get_book_by_id(book_id):
    """Return a book(Book objects) with a specific id."""
    
    book = Book.query.get(book_id)

    return book

def get_book_by_title(book_title):
    """Return a book(Book objects) with a specific title."""
    book_title = book_title.title()
    book = Book.query.filter(Book.book_title.like(f'%{book_title}%')).all()

    if book:
        return book
    else: 
        return None


def get_all_users():
    """Return list of all users(User objects)"""
    
    users = User.query.all()

    return users


def get_user_by_id(user_id):
    """Return a movie(Movie objects) with a specific id."""
    
    user = User.query.get(user_id)

    return user


def create_rating(user_id, book_id, rating_score):
    """Create and return a new rating."""

    rating = User_Rating(user_id=user_id,book_id=book_id,rating_score=rating_score)

    db.session.add(rating)
    db.session.commit()

    return rating

def get_rating_user_id(user_id):
    """Return list of all rating made by the user"""
    
    user_all_ratings = User_Rating.query.filter(User_Rating.user_id == user_id).all()

    return user_all_ratings



def add_favorite(user_id, book_id, date_add, comment):
    """Add book to favorite"""

    favorite_book = Favorite(user_id=user_id,book_id=book_id,date_add=date_add, comment=comment)

    db.session.add(favorite_book)
    db.session.commit()

    return favorite_book

def get_favorites_by_id(user_id):
    """Return list of all favorite books(Favorite objects)"""
    
    user_all_favorites = Favorite.query.filter(Favorite.user_id == user_id).all()

    return user_all_favorites

def delete_favorite(favorite_id):
    """Delete book from favorite"""

    delete_book = Favorite.query.filter(Favorite.favorite_id == favorite_id).first()

    db.session.delete(delete_book)
    db.session.commit()

    
def get_top_books(avg_rating):
    """Delete book from favorite"""

    top_books = Book.query.filter(Book.avg_rating > 4.50).all()

    return top_books




if __name__ == '__main__':
    from server import app
    connect_to_db(app)