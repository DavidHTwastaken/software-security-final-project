from flask import Blueprint, render_template, session, request, current_app, flash
from db import DB

sql_injection = Blueprint('sql_injection', __name__,
                          template_folder='templates', static_folder='static')
db = DB()
db.conn.autocommit = True


def handle_difficulty(query: str) -> tuple[str, str | None]:
    diff = session.setdefault('difficulty', 0)
    if diff == 0:
        pattern = f'{query.lower()}%'
        string = f"SELECT * FROM products WHERE LOWER(name) LIKE '{pattern}'"
        current_app.logger.info(string)
        return (string, None)
    if diff == 1:
        pattern = f'{query.lower()}%'
        string = f"SELECT * FROM products WHERE LOWER(name) LIKE '{pattern}'"
        return (string, None)
    if diff == 2:
        string = "SELECT * FROM products WHERE LOWER(name) LIKE %s"
        pattern = f'{query.lower()}%'
        return (string, pattern)


@sql_injection.route('/')
def index():
    query = request.args.get('query')
    try:
        if query:
            string, pattern = handle_difficulty(query)
            if pattern:
                db.cur.execute(string, (pattern,))
            else:
                db.cur.execute(string)
        else:
            db.cur.execute("SELECT * FROM products")
    except Exception as e:
        current_app.logger.error(e)
        flash(f'Error: {e}', 'error')
        return render_template('sql_injection.html')
    results = db.cur.fetchall()
    current_app.logger.info(f'Results: {results}')
    return render_template('sql_injection.html', results=results)


@sql_injection.post('/submit')
def submit():
    answer = request.json.get('answer')
    db.cur.execute("SELECT password FROM users WHERE username='admin';")
    real_answer = db.cur.fetchone()
    if real_answer and answer == real_answer['password']:
        return {'success': True}
    else:
        return {'success': False}


@sql_injection.errorhandler(500)
def handle_exception(e):
    current_app.logger.error(e)
    return render_template('error.html', error=e), 500
