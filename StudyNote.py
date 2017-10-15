import os
import markdown
import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, g
from app.note import Note

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

print(os.getcwd())

notes = []
DATABASE = 'note.db'


# 获取在 SQLite 中的数据
def get_note():
    new_notes = []
    cur = g.db.execute('SELECT * FROM Notes')
    for row in cur.fetchall():
        new_notes.append(Note(row[0], row[1]))
    return new_notes


# 往 SQLite 中插入 Note
def append_note(n_note):
    g.db.execute('INSERT INTO Notes (note_title, note_passage) VALUES (?, ?)', (n_note.title, n_note.passage))
    g.db.commit()


# 连接数据库
def connect_db():
    return sqlite3.connect(DATABASE)


# 连接数据库
@app.before_request
def before_request():
    g.db = connect_db()


# 关闭数据库连接
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


# 主页视图函数
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Note 应用界面
@app.route('/note', methods=['GET', 'POST'])
def note():
    global notes
    notes = get_note()
    if request.method == 'POST':
        title = request.form['title']
        passage = request.form['passage']

        if title not in notes:
            new_note = Note(title, markdown.markdown(passage))
            append_note(new_note)
            notes.append(new_note)
        else:
            flash('Title already exists!')
            redirect(url_for('note'))
    return render_template('note.html', notes=reversed(notes))


# 程序入口
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=3000
    )
