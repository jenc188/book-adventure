"""Seed Database"""

import csv, os
#from random import choice, randint
# from datetime import datetime
import model, crud, server


os.system('dropdb book-project')
os.system('createdb book-project')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/booksdata.csv', newline='') as csvfile:
    book_data = csv.DictReader(csvfile)

# Create books, store them in list so we can use them
# to create fake ratings later
    books_in_db = []
    for book in book_data:
        # get the title, authors,isbn, avg_rating, language_code, num_page from the book
        # dictionary.
        book_title = book['title']
        author = book['authors']
        avg_rating = book['average_rating']
        isbn = book['isbn']
        language_code= book['language_code']
        num_page= book['num_pages']

        
    
    #create a book and append it to books_in_db
        new_book = crud.create_book(book_title=book_title, author=author, isbn=isbn, avg_rating=avg_rating, language_code=language_code,num_page=num_page)
        books_in_db.append(new_book)
   

    for n in range(1,6):
        fullnames = ['','June Doe', 'Sam Smith', 'Michelle Town', 'Happy Adam', 'Ben Bright']
        fullname = fullnames[n].split()
        first_name = fullname[0]
        last_name = fullname[1]
        print(first_name)

        email = f'user{n}@test.com'  # Voila! A unique email!
        password = 'test'

        # create a user here
        new_user = crud.create_user(first_name, last_name, email, password)
        # create 10 ratings for the user

        