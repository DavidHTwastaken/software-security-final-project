from flask import Blueprint, render_template, session, request, current_app
from db import DB

sql_injection = Blueprint('sql_injection', __name__,
                          template_folder='templates', static_folder='static')
db = DB()
db.conn.autocommit = True


@sql_injection.route('/')
def index():
    query = request.args.get('query')
    if query:
        db.cur.execute(
            "SELECT * FROM products WHERE name LIKE %s", (query,))
    else:
        db.cur.execute("SELECT * FROM products")
    results = db.cur.fetchall()
    current_app.logger.info(f'Results: {results}')
    return render_template('sql_injection.html', results=results)


@sql_injection.post('/submit')
def submit():
    answer = request.form.get('answer')
    db.cur.execute("SELECT password FROM users WHERE username='admin';")
    real_answer = db.cur.fetchone()
    if real_answer and answer == real_answer[0]:
        return {'success': True}
    else:
        return {'success': False}
