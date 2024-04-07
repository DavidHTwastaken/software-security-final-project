from flask import Flask, render_template, request, jsonify
from db import DB


app = Flask(__name__)
db = DB()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = db.get_user(username, password)
    print(user)

    if user:
        return jsonify({'auth': True})
    else:
        return render_template('login.html', message='Invalid username or password.')
    
@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
