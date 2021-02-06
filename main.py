from flask import Flask, render_template, request
from app import create_app
from app.models import Book
from app.database import db
from script import *
from quickstart import *

app = create_app()
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def main():
    """Render the template with reload javascript funtion."""
    return render_template('home.html')


@app.route('/charge/', methods=['GET'])
def charge():
    """
    Call funtion to save all content book into the database.
    The goal of saving the books this way is to get better performance
    to get a random sentence.
    The particular configuration of database was chosen by its easy setup but
    maybe its not ideal for this project.
    """
    charge_books()
    return 'Finished'


@app.route('/download-books/', methods=['GET'])
def books_drive():

    download_books()
    return 'Finished'


@app.route('/show/', methods=['GET'])
def show():
    """Call phrase funtion."""
    sentence = Sentence(random_book())
    text = [sentence.sentence,  sentence.title, sentence.author]
    return render_template("show.html",
                           sentence=text[0],
                           title=text[1],
                           author=text[2]
                           )


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=False)
