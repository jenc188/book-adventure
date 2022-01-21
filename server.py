"""Server for book app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
import datetime



app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!
@app.route("/")
def render_homepage():
    """Render homepage."""

    return render_template("homepage.html")

@app.route("/books")
def show_all_books():
    books = crud.get_all_books()

    return render_template("all_books.html", books=books)


@app.route("/books/<book_id>")
def show_book_details(book_id):
   
    book = crud.get_book_by_id(book_id)
   
    return render_template("book_details.html", book=book)

@app.route("/users")
def show_all_users():
    users = crud.get_all_users()

    return render_template("all_users.html", users=users)


@app.route("/user/profile")
def show_user_details():
    
    logged_with_id = session.get("user_id")
    user = crud.get_user_by_id(logged_with_id)
    all_favorites = crud.get_favorites_by_id(logged_with_id)
    all_ratings = crud.get_rating_user_id(logged_with_id)

   
    return render_template("user_details.html", user=user,favorites=all_favorites, user_ratings=all_ratings)



@app.route("/users", methods=['POST'])
def create_user():
    """ Create User."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    user_password = request.form.get('user_password')

    user = crud.get_user_by_email(email)

    if not user:
        crud.create_user(first_name, last_name, email, user_password)
        message = "User created, please login"      
    else:
        message = "An account for this email already exists"

    flash(message)

    return redirect("/")

    
@app.route("/login", methods=['POST'])
def login_user():
    """ Login User."""

    email = request.form.get('email')
    user_password = request.form.get('user_password')

    user = crud.get_user_by_email(email)
    
    if not user or user.user_password != user_password:
        flash("The email or password is incorrect.")     
    else:
        #Log in user by storing the user's email in sesion
        session['user_id'] = user.user_id
        session['user_email'] = user.email
        flash(f'Logged in! Welcome back, {user.first_name}.')
        # user_session = session['user_email']
        # flash(f'Logged in! Welcome back, {user_session}.')

    return redirect("/")

@app.route("/logout")
def process_logout():
    """Log user out."""
    if session.get("user_id"):
        del session['user_email']
        del session['user_id']
        flash("You're logged out.")
    else: 
        flash("You're not logged in.")
    
    return redirect("/")


@app.route("/books/<book_id>/user_ratings", methods=['POST'])
def create_user_rating(book_id):
    """ Create User rating."""
    
    logged_with_email = session.get("user_email")
    
    rating_score = request.form.get('rating')
    
    if logged_with_email == False:
        flash("Please log in to rate a book.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else: 
        user= crud.get_user_by_email(logged_with_email)
        # user = crud.get_user_by_id(user_id)
        book = crud.get_book_by_id(book_id)
        book_rating = crud.create_rating(user.user_id, book.book_id, rating_score)
        flash(f"Your rating of this book is {rating_score} out of 5.")

    return redirect(f"/books/{book_id}")

@app.route("/books/<book_id>/favorites", methods=['POST'])
def add_to_favorite(book_id):
    """ Add to favorite list."""
    
    logged_with_email = session.get("user_email")
    adding_favorite = request.form.get('book_id')
    add_comment = request.form.get('comment')
    
    if logged_with_email == False:
        flash("Please log in to add to Favorite.")
        
    else: 
        user= crud.get_user_by_email(logged_with_email)
        # user = crud.get_user_by_id(user_id)
        book = crud.get_book_by_id(book_id)
        date_add = datetime.datetime.now()
        favorites = crud.add_favorite(user.user_id, book.book_id, date_add, add_comment)
        flash("Book added to your favorite list.")
  
    return render_template("favoritepage.html", favorites=favorites)

@app.route("/delete", methods=['POST'])
def delete_book_favorite():
    logged_with_email = session.get("user_email")
    user = crud.get_user_by_email(logged_with_email)
    

    favorite_delete = request.json.get('favoriteIdDelete')
    
    favorite_id_del= favorite_delete.split("-")[1]
    crud.delete_favorite(favorite_id_del)
    flash("Item has been deleted.")

    # if logged_with_email:
    #     book_delete = crud.delete_favorite(favorite_id)
    #     flash("Book deleted from favorite list. ")
    # else:
    #     flash("Please log in to delete from Favorite.")
    
    return {'sucess': True, 'status': "sucessfully deleted from favorite"}


@app.route("/top_books", methods=['GET'])
def get_top_rated_books(book_id, avg_rating):

    top_book_id = crud.get_book_by_id(book_id)
    top_books = crud.get_top_books(avg_rating)

    return render_template("top_books.html", books=top_book_id, top_books=top_books)


@app.route("/searchform", methods=['GET'])
def search_book():

    return render_template("searchpage.html")

@app.route("/searchbook", methods=['GET'])
def search_book_by_title():
    book_title = request.args.get('search-title')
    books = crud.get_book_by_title(book_title)
   

    if books == None:
        flash("Couldn't find book. Please try again.")
        return render_template("searchpage.html")
    else: 
         return render_template("all_books.html", books=books)





if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
