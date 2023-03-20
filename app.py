from flask import Flask, render_template, request, redirect, url_for
import os
import sys
from modules.questions import *
from modules.fileIO import *

# Flask Web App
app = Flask(__name__)

# index page
@app.route("/", methods=[ 'GET', 'POST' ])	# 'GET' and 'POST' are HTML methods that are used in the corresponding html file
def index():
	read_from_file()	# Initalize lists

	if request.method == 'POST':
		if request.form.get('log') == 'Login':	# This is a login button to take users to the login page
			return redirect(url_for('login'))
		elif request.form.get('sign') == 'Sign Up':	# This is a sign up button to take users to the sign up page
			return redirect(url_for('sign_up'))
	return render_template('index.html')

# login page
@app.route("/login", methods=[ 'GET', 'POST' ])
def login():
	error = None

	if request.method == 'POST':
		username = request.form['username']	# Get string entered into username field
		password = request.form['password']	# Get string entered into password field

		if username not in users and (username != 'admin' or password != 'admin'):	# Check if the username doesn't exist or isn't 'admin'
			error = 'Invalid credentials'	# If not, print error and prompt for input
		elif username != 'admin':
			idx = users.index(username)	# Get the index of the user in the three lists
			if password != passwords[idx]:	# Make sure it is the correct password for this user
				error = 'Incorrect password'
			else:
				return redirect(url_for('home', curruser = username))	# Go to home page, pass user index
		else:
			return redirect(url_for('home', curruser = username))	# Go to home, pass -1 index (admin)

	return render_template('login.html', error=error)

# sign up page
@app.route("/sign_up", methods=[ 'GET', 'POST' ])
def sign_up():
	error = None

	if request.method == 'POST':
		username = request.form['username']	# Get username
		password = request.form['password']	# Get password
		confirm = request.form['confirm']	# Get password again to confirm

		if username in users:	# Check if username is already in 'users.txt'
			error = 'Username taken'
		else:
			if (password == confirm):	# Check that the entered password and the re-entered passwords match
				# Add the username, password, and highscore to their respective lists
				users.append(username)
				passwords.append(password)
				highscores.append(0)
				append_to_file()	# Add the new user with their password and 0 highscore to the end of 'users.txt'
				
				return redirect(url_for('home', curruser = username))	# If successful, go to the home page and pass user index
			else:	# Throw error if passwords don't match
				error = 'Passwords do not match'

	return render_template('sign-up.html', error=error)

# home page
@app.route("/home/<curruser>", methods=[ 'GET', 'POST' ])
def home(curruser):
	if request.method == 'POST':
		if request.form.get('ind') == 'Logout':  # This is a login button to take users to the login page
			return redirect(url_for('index'))

	return render_template('home.html', currentuser = curruser)

@app.route("/easyGame")#, methods=[ 'GET', 'POST' ])	# 'GET' and 'POST' are HTML methods that are used in the corresponding html file
def play_easyGame():
	listOfQuestions = []
	ret = get_easyQuestion(listOfQuestions)
	listOfQuestions.append(ret[5])
	print(ret)

	return render_template('easyquiz.html', question=ret[0], answer1=ret[1], answer2=ret[2], answer3=ret[3], answer4=ret[4])

if __name__ == "__main__":
	port = 5000
	if(len(sys.argv) >= 2):
		port = sys.argv[1]
	app.run('0.0.0.0', port)	# 5000 is the port for the url, change this when test so that multiple devs can run at same time on different ports
