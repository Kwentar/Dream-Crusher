from flask import Flask, render_template, request, session, flash, redirect, url_for
app = Flask(__name__)


SECRET_KEY = 'development key'
app.secret_key = SECRET_KEY


@app.route('/')
def index():
    username = session['username'] if 'username' in session else None
    return render_template("index.html", username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid username'
        elif request.form['password'] != 'admin':
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
