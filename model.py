"""Models for book app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Data model for a user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    user_password = db.Column(db.String)
    
    user_favorite = db.relationship("Favorite", back_populates="favorite_user")

    user_user_rating = db.relationship("User_Rating", back_populates="user_ratings_user")

    def __repr__(self):
        """Provide useful output when printing."""

        return f'<User user_id={self.user_id} first_name={self.first_name} last_name={self.last_name} email={self.email}>'


class Favorite(db.Model):
    """Data model for a favorite"""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    date_add = db.Column(db.Date)
    comment = db.Column(db.String)
    
    favorite_user = db.relationship("User", back_populates="user_favorite")

    favorite_book = db.relationship("Book", back_populates="book_favorite")

    def __repr__(self):
        """Provide useful output when printing."""

        return f'<Favorite favorite_id={self.favorite_id} book_id={self.book_id} user_id={self.user_id} date_add={self.date_add}>'


class User_Rating(db.Model):
    """Data model for a user_rating"""

    __tablename__ = "user_ratings"

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    rating_score = db.Column(db.Integer)
    

    user_ratings_user = db.relationship("User", back_populates="user_user_rating")

    user_rating_book = db.relationship("Book", back_populates="book_user_rating")

    def __repr__(self):
        """Provide useful output when printing."""

        return f'<User_Rating rating_id={self.rating_id} user_id={self.user_id} book_id={self.book_id} rating_score={self.rating_score}>'



class Book(db.Model):
    """Data model for a book"""

    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_title = db.Column(db.String)
    author= db.Column(db.String)
    isbn = db.Column(db.String)
    num_page = db.Column(db.String)
    language_code = db.Column(db.String)
    avg_rating = db.Column(db.String)

    book_user_rating = db.relationship("User_Rating", back_populates="user_rating_book")

    book_favorite = db.relationship("Favorite", back_populates="favorite_book")

    def __repr__(self):
        """Provide useful output when printing."""

        return f'<Book book_id={self.book_id} book_title={self.book_title} avg_rating={self.avg_rating}>'



def connect_to_db(flask_app, db_uri="postgresql:///book-project", echo=True):

    """Connect the database to our Flask app."""

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)