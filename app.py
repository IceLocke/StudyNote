import os
import markdown
import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, g, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

notes = []
DATABASE = 'note.db'


class Note:
    def __init__(self, title, passage):
        self.title = title
        self.passage = passage
        

# 获取在 SQLite 中的数据
def get_note():
    new_notes = []
    cur = g.db.execute('SELECT * FROM Notes')
    for row in cur.fetchall():
        new_notes.append(Note(row[0], markdown.markdown(row[1])))
    return new_notes


# 获取在 SQLite 中原始数据
def get_raw_note(name):
    cur = g.db.execute('SELECT * FROM Notes WHERE note_title = ?', (name,))
    got_note = cur.fetchall()

    if len(got_note) != 0:
        got_note = got_note[0]
    else:
        return False

    return Note(got_note[0], got_note[1])


# 获取单一的 Note
def get_single_note(name):
    cur = g.db.execute('SELECT * FROM Notes WHERE note_title = ?', (name,))
    got_note = cur.fetchall()

    if len(got_note) != 0:
        got_note = got_note[0]
    else:
        return False

    return Note(got_note[0], markdown.markdown(got_note[1]))


# 往 SQLite 中插入 Note
def append_note(n_note):
    g.db.execute('INSERT INTO Notes (note_title, note_passage) VALUES (?, ?)', (n_note.title, n_note.passage))
    g.db.commit()


# 删除 SQLite 中的 Note
def delete_note(notename):
    g.db.execute('DELETE FROM Notes WHERE note_title = ?', (notename,))
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
            new_note = Note(title, passage)
            append_note(new_note)
            notes.append(new_note)

        else:
            flash('Title already exists!')
            redirect(url_for('note'))
    notes = get_note()
    return render_template('note.html', notes=reversed(notes))


# 单个Note
@app.route('/note/<name>', methods=['GET', 'POST'])
def notepage(name):
    if request.method == 'GET':
        single_note = get_single_note(name)
        if single_note is not False:
            return render_template('notepage.html', note=single_note)
        else:
            abort(404)
        return
    elif request.method == 'POST':
        notename = request.form['DELETE']
        delete_note(notename)
        return redirect(url_for('note'))


# 编辑Note
@app.route('/note/edit/<name>', methods=['GET', 'POST'])
def editnote(name):
    if request.method == 'GET':
        single_note = get_raw_note(name)
        if single_note is not False:
            return render_template('noteedit.html', note=single_note)
        else:
            abort(404)
    elif request.method == 'POST':
        notename = request.form['name']
        notepassage = request.form['passage']
        delete_note(notename)
        append_note(Note(notename, notepassage))
        return redirect(url_for('note'))


# 程序入口
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=3000
    )
