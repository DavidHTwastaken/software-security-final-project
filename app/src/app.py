from flask import Flask, render_template, request, jsonify
from db import DB
from flask_login import current_user


app = Flask(__name__)
db = DB()


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('bugs.html')
    else:
        return render_template('login.html')
    


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
            return jsonify({'auth': True}) 
    except Exception as e:
        print(e)
        return jsonify({'auth': False})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
