import os
from flask import Flask, render_template, g, request, session, redirect, url_for
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'postgres_db_cur'):
        g.postgres_db_cur.close()

    if hasattr(g, 'postgres_db_conn'):
        g.postgres_db_conn.close()


def get_current_user():
    user_result = None

    if 'user' in session:
        user = session['user']

        db = get_db()
        db.execute('SELECT id, name, password, expert, admin from users where name = %s', (user, ))
        user_result = db.fetchone()

    return user_result


@app.route('/')
def index():
    user = get_current_user()

    return render_template('home.html', user=user)


@app.route('/register', methods=['POST', 'GET'])
def register():
    user = get_current_user()

    if request.method == 'POST':

        db = get_db()
        hashed_password = generate_password_hash(request.form['password'], method='sha256')

        db.execute('INSERT INTO users (name, password, expert, admin) values (%s, %s, %s, %s)', (request.form['name'], hashed_password, '0', '0', ))

        return '<h1>User created!</h1>'

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = get_current_user()

    if request.method == 'POST':

        db = get_db()

        name = request.form['name']
        password = request.form['password']

        db.execute('SELECT id, name, password from users where name = %s', (name, ))
        user_result = db.fetchone()

        if check_password_hash(user_result['password'], password):
            session['user'] = user_result['name']
            return '<h1>The password is correct!</h1>'
        else:
            return '<h1>The password is incorrect!</h1>'


    return render_template('login.html')


@app.route('/question')
def question():
    user = get_current_user()

    return render_template('question.html')


@app.route('/answer')
def answer():
    user = get_current_user()

    return render_template('answer.html')


@app.route('/ask')
def ask():
    user = get_current_user()

    return render_template('ask.html')


@app.route('/unanswered')
def unanswered():
    user = get_current_user()

    return render_template('unanswered.html')


@app.route('/users')
def users():
    user = get_current_user()

    return render_template('users.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
