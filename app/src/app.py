import logging
import sys
from flask import Flask, flash, make_response, render_template, request, jsonify, session, redirect, url_for
from db import DB
from services.shop import Shop
from sql_injection import sql_injection
from services.models import create_db_schema

app = Flask(__name__)
db = DB()
app.secret_key = b'83b1188d5ce6cdccd04d037ed9fec28c14836710841762555675f7d3e999e4d8'
app.register_blueprint(sql_injection, url_prefix='/sqli')
create_db_schema()

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

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
        # balance = db.get_balance(username).get('balance')
        # balance = float(balance)

        # app.logger.info(f'The balance is {balance}')
        app.logger.info(f'Result from database for login attempt: {user}')

        if user:
            session['difficulty'] = '0'
            session['username'] = username
            session['difficulty_name'] = "No Security"

            app.logger.info(f'The current difficulty is {session['difficulty']} of type {type(session.get('difficulty'))}')
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
            session['difficulty'] = '0'
            session['username'] = username
            session['difficulty_name'] = "No Security"

            app.logger.info(f'The current difficulty is {session['difficulty']} of type {type(session.get('difficulty'))}')
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

        app.logger.info(f'The current difficulty is {session['difficulty']} of type {type(session.get('difficulty'))}')
        return render_template('difficulty.html')
    else:
        return render_template('difficulty.html')


@app.route('/html_injection', methods=['GET', 'POST'])
def html_injection():
    if request.method == 'POST':
        user_input = request.form.get('post')
        return user_input
    return render_template('html_injection.html')
'''
[{
        "id":1,
        "name":"banana",
        "price":5.00,
        "date":"4-12-2024"
        }]
'''
@app.route('/shop',methods=['GET', 'POST'])
def shop():
    if 'POST' == request.method:
        session_token = Shop.login(request.form['username'],request.form['password'])
        if session_token:
            response = make_response(redirect('/shop'))
            response.set_cookie("shop_token",session_token)
            return response
        else:
            return render_template('shop_login.html', error="Invalid username or password")
    else:
        session_token = request.cookies.get("shop_token")

        if session_token and len(session_token) > 5:
            if '2' == session.get('difficulty'):
                loggedIn, balance, inventory, username = Shop.get_user2(session_token)
            else:
                loggedIn, balance, inventory, username = Shop.get_user(session_token)
            
            if not loggedIn:
                response = make_response(redirect('/shop'))
                response.set_cookie("shop_token","")
                return response
            
            return render_template('race_condition.html',balance=balance,inventory=inventory, username=username)
        return render_template('shop_login.html')
            
    # inventory = db.get_inventory_for_user(session['username'])
    # balance = session.get('balance')
    # # # error = request.args.get('race_error') if None != request.args.get('race_error') else ""

    # # app.logger.info(f"race_error: {error}")
    # return render_template('race_condition.html',balance=balance,inventory=inventory)


@app.route('/buy/<id>', methods=["POST"])
def buy(id: int):
    cookies = request.cookies
    token = cookies.get('shop_token')
    if '2' == session.get('difficulty'):
        error = Shop.buy2(token, id)
    else:
        error = Shop.buy(token, id)
    

    if error == "":
        return make_response(redirect('/shop'))
    else:
        app.logger.info(f"race_error: {error}")
        return error


@app.route('/sell/<id>', methods=["POST"])
def sell(id: int):
    cookies = request.cookies
    token = cookies.get('shop_token')
    if '2' == session.get('difficulty'):
        error = Shop.sell2(token, id)
    else:
        error = Shop.sell(token, id)

    if error == "":
        return make_response(redirect('/shop'))
    else:
        app.logger.info(f"race_error: {error}")
        return error


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",threaded=True)
