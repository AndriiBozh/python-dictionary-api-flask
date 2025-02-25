from xml.sax.saxutils import escape

from flask import Flask
from flask import render_template
import pandas as pd
import dotenv

filepath = dotenv.get_key('.env', 'FILE_PATH')
df = pd.read_csv(filepath)

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/<word>')
def get_word_definition(word):
    # get index of a row, by the value of a cell in a 'word' column
    row_index = df.index[df['word'] == word]
    print(row_index)
    # get definition by index of a row and column name and
    # convert it to list, so than it could be converted to JSON
    definition = list(df.loc[row_index, 'definition'])
    return {
        "definition": definition,
        #     any user - provided values rendered in the output must be escaped to protect
        # from injection attacks
        "word": escape(word)
    }


# custom 'not found page'
@app.errorhandler(404)
def not_found(err):  # err => 404 argument below
    return render_template(
        'notfound.html'), 404  # 404 tells Flask that the status code of that page should be 404 which means not found.


# If the :attr:`debug` flag is set the server will automatically
# reload for code changes and show a debugger in case an exception happened.
app.run(debug=True)
