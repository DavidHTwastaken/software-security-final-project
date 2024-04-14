from flask import Blueprint, render_template, session, request
from db import DB

sql_injection = Blueprint('sql_injection', __name__,
                          template_folder='templates', static_folder='static')
db = DB()
db.conn.autocommit = True


@sql_injection.route('/')
def index():
    return render_template('sql_injection.html')


@sql_injection.post('/submit')
def submit():
    answer = request.form.get('answer')
    db.cur.execute("SELECT password FROM users WHERE username='admin';")
    real_answer = db.cur.fetchone()
    if real_answer and answer == real_answer[0]:
        return {'success': True}
    else:
        return {'success': False}
