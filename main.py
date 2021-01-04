from flask import Flask, render_template, request
from script import *


def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app


app = create_app()


@app.route('/', methods=['GET'])
def main():
    return render_template('home.html')


@app.route('/ajax/', methods=['GET'])
def show():
    text = phrase(epub_to_text(get_ebooks()))
    return render_template("show.html",
                           sentence=text[0],
                           author=text[1]
                           )


if __name__ == '__main__':
    app.run()
