from flask import Flask, render_template, request, redirect, flash, session, url_for
from API.users import Users  # Import the Users class

app = Flask(__name__)
app.secret_key = 'ISkjdSd657Sd65Sdjhjsdaow'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('my_account'))

    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        if Users.authenticate_user(username_or_email, password):
            session['username'] = Users.get_username_from_email(
                username_or_email) if '@' in username_or_email else username_or_email
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


def is_logged_in():
    return 'username' in session


@app.route('/register', methods=['GET', 'POST'])
def register():
    if is_logged_in():
        return redirect('/my_account')

    if request.method == 'POST':
        user_data = {
            "email": request.form['email'],
            "username": request.form['username'],
            "password": request.form['password']  # In real applications, hash this password
        }

        response, status_code = Users.create_user(user_data)

        if status_code == 201:  # Successful creation
            session['username'] = user_data['username']  # Auto login after registration
            flash('Account created and logged in successfully', 'success')
            return redirect('/')
        else:
            flash('Registration failed', 'error')
            return redirect('/register')

    return render_template('register.html')


@app.route('/my_account')
def my_account():
    if not is_logged_in():
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Render the my-account page template
    return render_template('my_account.html')


@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))  # Redirect to login page or home page


if __name__ == '__main__':
    app.run(debug=True)
