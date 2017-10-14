import os
import markdown
from flask import Flask, render_template, request, flash, redirect, url_for
from note import Note

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

notes = []


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/note', methods=['GET', 'POST'])
def note():
    if request.method == 'POST':
        title = request.form['title']
        passage = request.form['passage']
        if title not in notes:
            notes.append(Note(title, markdown.markdown(passage)))
        else:
            flash('Title already exists!')
            redirect(url_for('note'))

    return render_template('note.html', notes=reversed(notes))


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000
    )
