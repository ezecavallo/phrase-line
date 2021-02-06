import os
import random
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import nltk
from app.database import db
from app.models import Book
from sqlalchemy.sql.expression import func, select


class Sentence():
    """Class model for Sentence"""

    def __init__(self, object):
        self.sentence = self.get_sentences(object.content)
        self.title = object.title
        self.author = object.author

    def get_sentences(self, text):
        sentences = nltk.sent_tokenize(text)
        return self.random_phrase(sentences)

    def random_phrase(self, sentences):
        sentence = random.choice(sentences)
        if len(sentence) < 15:
            return self.random_phrase(sentences)
        else:
            return sentence

    def __str__(self):
        return f'{self.sentence} in {self.title} by {self.author}'


def random_book():
    book = db.session.query(Book).order_by(func.random()).first()
    return book


def get_ebooks():
    """Return path with a random book from the main folder."""
    path = "books-test/"
    books = []

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            books.append(os.path.join(root, name))
    ebookspath = random.choice(books)
    return books


def random_book():
    book = db.session.query(Book).order_by(func.random()).first()
    return book


def epub_to_html(epub_path):
    """
    Get html from epub books.
    This function search for all html items inside the .zip/.epub
    Verify if the book already exist in database,
    if not create without exception list.
    """
    global author, title
    book = epub.read_epub(epub_path)

    title = "".join(book.get_metadata('DC', 'title'))
    author = "".join(book.get_metadata('DC', 'creator'))
    query = Book.query.filter_by(title=title).first()
    if not query:
        text = []
        exception_list = ['Text/cubierta.xhtml', 'Text/autor.xhtml', 'Text/info.xhtml',
                          'Text/sinopsis.xhtml', 'Text/notas.xhtml', 'Text/titulo.xhtml',
                          'Text/apendices.xhtml', 'Text/anotaciones.xhtml',
                          'Text/agradecimientos.xhtml', 'Text/map_001.xhtml',
                          'Text/map_001.xhtml', 'Text/map_002.xhtml', 'Text/map_003.xhtml',
                          'Text/map_004.xhtml', 'Text/map_005.xhtml', 'Text/map_001.xhtml',
                          'Text/capi_atk.xhtml', 'Text/Bibliografia.xhtml', 'Text/GuiadelLector.xhtml',
                          'Text/Info.xhtml', 'Text/Titulo.xhtml', 'Text/Sinopsis.xhtml',
                          'Text/Prologo.xhtml', 'Text/Notas.xhtml', 'Text/Cubierta.xhtml',
                          'Text/Autor.xhtml']

        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                if item.get_name() not in exception_list:
                    text.append(item.get_content())

        book = Book(title=title, author=author, content=to_text(text))
        db.session.add(book)
        db.session.commit()
        print('Guardado')
    else:
        print('Already in')
        str = nltk.sent_tokenize(query.content)
        ret = random.choice(str)
        print(ret)
        return ret


def charge_books():
    books = get_ebooks()
    for book in books:
        print(book)
        to_database = epub_to_html(book)
        print('Yay!')


def to_text(html):
    """
    Decode data in UTF-8 format and get all <p> tag.
    """
    to_parse = []
    str = b''.join(html)
    # decoder = str.decode('utf-8')
    soup = BeautifulSoup(str, 'html.parser')
    for tag in soup.find_all(("p")):

        if len(tag.text) > 4:
            to_parse.append(tag.text)

    parsed = list(filter(None, to_parse))
    joined = ''.join(parsed)
    return joined


def phrase(book):
    text = nltk.sent_tokenize(book.content)
    text_r = random.choice(text)
    author = book.author
    if len(text) > 50:
        return [text_r, author]
    else:
        return phrase(random_book())
