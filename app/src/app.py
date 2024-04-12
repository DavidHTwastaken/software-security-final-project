from flask import Flask, flash, render_template, request, jsonify, session, redirect, url_for
from db import DB

app = Flask(__name__)
db = DB()
app.secret_key = b'83b1188d5ce6cdccd04d037ed9fec28c14836710841762555675f7d3e999e4d8'


@app.route('/')
def index():
    if 'username' in session:
        app.logger.info('logged in')
        return redirect(url_for('bugs'))
    else:
        return redirect(url_for('login'))


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.form
        username = data.get('username')
        password = data.get('password')

        user = db.get_user(username, password)
        app.logger.info(f'Result from database for login attempt: {user}')

        if user:
            session['difficulty'] = 0
            session['username'] = username

            session['difficulty_name'] = "No Security"

            return redirect(url_for('bugs'))
        else:
            flash("Login failed")
            return redirect(url_for('login'), 401)

    except Exception as e:
        app.logger.error(f"An error occurred when logging in: {e}")


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/register', methods=["POST"])
def register():
    try:
        data = request.form
        username = data.get('username')
        password = data.get('password')

        user_created = db.add_user(username, password)
        app.logger.info(f'Result from add_user: {user_created}')

        if user_created:
            session['difficulty'] = 0
            session['username'] = username

            session['difficulty_name'] = "No Security"

            return redirect(url_for('bugs'))
        else:
            flash("Registration failed")
            return redirect(url_for('register'), 401)
    except Exception as e:
        print(e)
        return jsonify({'auth': False, 'error': e})


@app.route('/bugs')
def bugs():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('bugs.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/difficulty', methods=['POST', 'GET'])
def difficulty():
    if request.method == 'POST':
        difficulty = request.form.get('difficulty')
        session['difficulty'] = difficulty

        if session['difficulty'] == '0':
            session['difficulty_name'] = "No Security"
        elif session['difficulty'] == '1':
            session['difficulty_name'] = "Some Security"
        elif session['difficulty'] == '2':
            session['difficulty_name'] = "Maximum Security"
    
        return render_template('difficulty.html')
    else:
        return render_template('difficulty.html')

@app.route('/html_injection', methods=['GET', 'POST'])
def html_injection():
    if request.method == 'POST':
        user_input = request.form['input']
        # Process the user input here
        # Example: save to database, sanitize input, etc.
        return "Input received: " + user_input
    return render_template('html_injection.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
