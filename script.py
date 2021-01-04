import os
import random
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import nltk


def get_ebooks():
    """Return path with a random book from the main folder."""
    path = "Libros/"
    books = []

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            books.append(os.path.join(root, name))
    ebookspath = random.choice(books)
    return ebookspath


def epub_to_html(epub_path):
    """
    Get html from epub books.
    This function search for all html items inside the .zip/.epub
    Then select a random .html, get its content and return it.
    """
    global author, title
    book = epub.read_epub(epub_path)

    title = "".join(book.get_metadata('DC', 'title'))
    author = "".join(book.get_metadata('DC', 'creator'))
    chapters = []
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
                chapters.append(item.get_name())

    item_book = random_choice(chapters)
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            if item.get_name() == item_book:
                text.append(item.get_content())
    return text


def parserdata(chap):
    """
    Decode data in UTF-8 format and get all <p> tag.
    """
    parsed = []
    str = b"".join(chap)
    decoder = str.decode('utf-8')
    soup = BeautifulSoup(decoder, 'html.parser')
    for tag in soup.find_all(re.compile("p")):
        parsed.append(tag.string)
    return parsed


def epub_to_text(epub_path):
    """Call function to get plain text."""
    chapters = epub_to_html(epub_path)
    text = parserdata(chapters)
    return text


def random_choice(text):
    try:
        return random.choice(text)
    except:
        return phrase(epub_to_text(get_ebooks()))


def check_data(data):
    text = random_choice(data)
    while text is None:
        return check_data(data)
    return text


def phrase(str):
    checked_data = check_data(str)
    o = nltk.sent_tokenize(checked_data)
    k = random.choice(o)
    if len(k) > 50:
        return [k, author]
    else:
        return phrase(epub_to_text(get_ebooks()))
