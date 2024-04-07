from flask import Flask, render_template, request, jsonify
from db import DB


app = Flask(__name__)
db = DB()


@app.route('/')
def index():
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
        return jsonify({'auth': False})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
