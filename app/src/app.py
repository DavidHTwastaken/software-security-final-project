from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from db import DB


app = Flask(__name__)
db = DB()
app.secret_key = b'83b1188d5ce6cdccd04d037ed9fec28c14836710841762555675f7d3e999e4d8'


@app.route('/')
def index():
    if 'username' in session:
        app.logger.info('logged in')
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
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'), 401)
    except Exception as e:
        app.logger.error(f"An error occurred when logging in: {e}")


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/register', methods=["POST"])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user_created = db.add_user(username, password)
        print(user_created)

        if user_created:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('register'), 401)
    except Exception as e:
        print(e)
        return jsonify({'auth': False})
    
@app.route('/bugs')
def bugs():
    return render_template('bugs.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/difficulty')
def difficulty():
    return render_template('difficulty.html')

@app.route('/logout')
def logout():
    return "hello"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
