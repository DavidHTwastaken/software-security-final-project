from flask import Flask, render_template, request, jsonify
from db import DB
import flask_login

login_manager = flask_login.LoginManager()


app = Flask(__name__)
db = DB()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = db.get_user(username, password)
        app.logger.info(f'Result from database for login attempt: {user}')

        if user:
            return jsonify({'auth': True})
        else:
            return jsonify({'auth': False})
    except Exception as e:
        app.logger.error(f"An error occurred when logging in: {e}")


@app.get('/register')
def register_page():
    return render_template('register.html')


@app.post('/register')
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user_created = db.add_user(username, password)
        print(user_created)

        if user_created:
            return render_template('login.html', message='User created successfully.')
    except Exception as e:
        print(e)
        return render_template('register.html', message='An error occurred during registration: {e}')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
