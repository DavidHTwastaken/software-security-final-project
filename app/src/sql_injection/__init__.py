from flask import Blueprint, render_template, session
from db import DB

sql_injection = Blueprint('sql_injection', __name__,
                          template_folder='templates')
db = DB()


@sql_injection.route('/')
def index():
    return render_template('sql_injection.html')
