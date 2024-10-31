from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for sessions

USER_DATA_FILE = "user_data.txt"  # File to store user credentials

# Hash passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register new user
def register_user(username, password):
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hash_password(password)}\n")

# Verify credentials for login
def verify_credentials(username, hashed_password):
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(",")
            if stored_username == username and stored_password == hashed_password:
                return True
    return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if user exists
        if verify_credentials(username, hash_password(password)):
            flash("User already exists!")
        else:
            register_user(username, password)
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_credentials(username, hash_password(password)):
            session['username'] = username  # Set session
            return redirect(url_for('secure_page'))
        else:
            flash("Invalid username or password.")
    return render_template('login.html')

@app.route('/secure-page')
def secure_page():
    if 'username' in session:
        return f"Welcome to the secure page, {session['username']}!"
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
