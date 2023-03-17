from flask import Flask, render_template, request, redirect, url_for
import os

USERFILE_PATH = 'static/users.txt'	# 'users.txt' path
users = []; passwords = []; highscores = []	# Declare lists for users, passwords, and highscores

# Read usernames, passwords, and highscores from 'users.txt' file, then add them to the lists
def read_from_file():
	rfile = open(USERFILE_PATH, 'r')	# Open users file to read in data
	users.clear(); passwords.clear(); highscores.clear()	# Clear the lists (just in case)

	for line in rfile:
		currline = line.split(',')	# Split line of users.txt by commas
		users.append(currline[0])	# Add usernames to users list
		passwords.append(currline[1])	# Add passwords to password list
		highscores.append(int(currline[2]))	# Add (integer) highscores to highscores list

	rfile.close()	# Close the read file

# Append a line to the end of 'users.txt'
def append_to_file():
	idx = len(users) - 1
	newline = users[idx] + ',' + passwords[idx] + ',' + str(highscores[idx]) + '\n'	# String to be appended to 'users.txt'

	afile = open(USERFILE_PATH, 'a')	# Open 'users.txt' to be appended to
	afile.write(newline)	# Append the newline to the end of the file
	afile.close()	# Close file

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
	elif request.method == 'GET':
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
		elif username != 'admin' or password != 'admin':
			idx = users.index(username)	# Get the index of the username for the three lists
			if password != passwords[idx]:	# Make sure it is the correct password for this user
				error = 'Incorrect password'
			else:
				return redirect(url_for('home'))	# If successful, take to home page
		else:
			return redirect(url_for('home'))

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
				users.append(username)
				passwords.append(password)
				highscores.append(0)
				append_to_file()	# Add the new user with their password and 0 highscore to the end of 'users.txt'
				return redirect(url_for('home'))	# If successful, go to the home page
			else:	# Throw error if passwords don't match
				error = 'Passwords do not match'

	return render_template('sign-up.html', error=error)

# home page
@app.route("/home", methods=[ 'GET', 'POST' ])
def home():
	return render_template('home.html')

if __name__ == "__main__":
	app.run('0.0.0.0', 5000)	# 5000 is the port for the url, change this when test so that multiple devs can run at same time on different ports
