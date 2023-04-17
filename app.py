from flask import Flask, render_template, request, redirect, url_for, session
import sys
from modules.questions import *
from fileIO import *
import pandas as pd
import importlib


TEMPLATES_AUTO_RELOAD = True

MAXQUESTIONS = 5
MINQUESTIONS = 2
app = Flask(__name__)

easyQuestions = pd.read_csv('static/easyQuestions.csv')
mediumQuestions = pd.read_csv('static/mediumQuestions.csv')
hardQuestions = pd.read_csv('static/hardQuestions.csv')

# index page
@app.route("/", methods=[ 'GET', 'POST' ])	# 'GET' and 'POST' are HTML methods that are used in the corresponding html file
def index():
	read_from_file()
	curruser = session.get('curruser', None)

	if request.method == 'POST':
		# Go to login page
		if request.form.get('log') == 'Login':
			return redirect(url_for('login'))
		# go to sign up page
		elif request.form.get('sign') == 'Sign Up':
			return redirect(url_for('sign_up'))
		# Go straight to home
		elif request.form.get('skip') == 'Home':
			# Throw error if not logged in
			if not curruser:
				error = 'Currently not logged in.'
				return render_template('index.html', error=error)
			else:
				return redirect(url_for('home'))
	return render_template('index.html', error=None)

def toBinary(a):
	l,m=[],[]
	for i in a:
		l.append(ord(i))
	for i in l:
		m.append(int(bin(i)[2:]))
	return m

# login page
@app.route("/login/", methods=[ 'GET', 'POST' ])
def login():
	error = None

	if request.method == 'POST':
		username = request.form['username']	# Get string entered into username field
		password = request.form['password']	# Get string entered into password field

		if username not in users and (username != 'admin' or password != 'admin'):	# Check if the username doesn't exist or isn't 'admin'
			error = 'Invalid credentials'	# If not, print error and prompt for input
		elif username != 'admin':
			idx = users.index(username)	# Get the index of the user in the three lists
			read_from_file()

			if password != passwords[idx]:	# Make sure it is the correct password for this user
				error = 'Incorrect password'
			else:
				session['curruser'] = username
				session.permanent = False
				return redirect(url_for('home'))	# Go to home page, pass user index
		else:
			session['curruser'] = username
			return redirect(url_for('home'))	# Go to home, pass -1 index (admin)

	return render_template('login.html', error=error)

# sign up page
@app.route("/sign_up/", methods=[ 'GET', 'POST' ])
def sign_up():
	error = None

	if request.method == 'POST':
		username = request.form['username']	# Get username
		password = request.form['password']	# Get password
		confirm = request.form['confirm']	# Get password again to confirm

		if username in users:	# Check if username is already in 'users.txt'
			error = 'Username taken'
		else:
			if password == confirm:	# Check that the entered password and the re-entered passwords match
				# Add the username, password, and highscore to their respective lists
				users.append(username)
				passwords.append(password)
				highscoresE.append(0)
				highscoresM.append(0)
				highscoresH.append(0)
				append_to_file()	# Add the new user with their password and 0 highscore to the end of 'users.txt'
				session['curruser'] = username
				return redirect(url_for('home'))	# If successful, go to the home page and pass user index
			else:	# Throw error if passwords don't match
				error = 'Passwords do not match'

	return render_template('sign-up.html', error=error)

@app.route("/change_password/", methods=[ 'GET', 'POST' ])
def change_password():
	curruser = session.get('curruser', None)
	idx = users.index(curruser)  	# Index of the curruser in the lists
	error = None

	if not curruser:
		return redirect(url_for('index'))

	if request.method == 'POST':
		currpass = request.form['currpass']
		newpass = request.form['newpass']
		newconfirm = request.form['newconfirm']

		if request.form.get('exit') == 'Exit':  	# Return to home
			return redirect(url_for('home'))
		if currpass == passwords[idx]:  # Check that current password is correct
			if newpass == newconfirm:  # Confirm new password
				if newpass != currpass:
					passwords[idx] = newpass
					resave_file()
					return redirect(url_for('home'))
				else:
					error = 'New password cannot be the same as your old password'
			else:
				error = 'New passwords do not match'
		else:
			error = 'Incorrect current password'

	return render_template('change-pass.html', error=error)

# home page
@app.route("/home/", methods=[ 'GET', 'POST' ])
def home():
	curruser = session.get('curruser', None)

	# If user not logged in, sent back to index
	if not curruser:
		return redirect(url_for('index'))

	if request.method == 'POST':
		if request.form.get('ind') == 'Logout':  # Logout button (send to index)
			return redirect(url_for('index')) #redirect to main page
		if request.form.get('play') == 'play':  # Check if 'play' was hit
			return redirect(url_for('play')) #redirect to play page
		if request.form.get('change-pass') == 'Change Password':  	# Redirect to change password page
			return redirect(url_for('change_password'))

	return render_template('home.html', currentuser = curruser)

# home page
@app.route("/play/", methods=[ 'GET', 'POST' ])
def play():
	global numQuestions #get number of questions
	curruser = session.get('curruser', None)

	if not curruser:
		return redirect(url_for('index'))

	if request.method == 'POST':
		if request.form.get('go'):
			if request.form.get('go') == 'Exit':  # This is a login button to take users to the login page
				return redirect(url_for('home')) #Redirect to /home
			else:
				numQ = request.form['numQ']	# Get username


				if numQ.isdigit():  # checks if numQ is comprised of digits.
					numQ = int(numQ)  # if it is digits it is converted to an int
					if MINQUESTIONS <= numQ <= MAXQUESTIONS:  # checks if numQ is within bounds
						numQuestions = numQ
					else:
						errorStatement = "Please enter valid number..."  # statement to be passed to play.html
						return render_template("play.html", errorStatement=errorStatement, min=MINQUESTIONS, max=MAXQUESTIONS)
				else:
					errorStatement = "Please enter valid number..."  # if it isnt error statment is ran to try again
					return render_template("play.html", errorStatement=errorStatement, min=MINQUESTIONS, max=MAXQUESTIONS)

				session['numQuestions'] = numQuestions #Save to session
				session['currentQuestion'] = 1 #reset current question counter
				session['score'] = 0 #Reset score
				if request.form.get('go') == 'GO (easy difficulty)':  # This is a login button to take users to the login page
					return redirect(url_for('play_game', gametype='easy')) #Redirect to /easyGame
				elif request.form.get('go') == 'GO (medium difficulty)':  # This is a login button to take users to the login page
					return redirect(url_for('play_game', gametype='medium')) #Redirect to /easyGame
				elif request.form.get('go') == 'GO (hard difficulty)':  # This is a login button to take users to the login page
					return redirect(url_for('play_game', gametype='hard')) #Redirect to /easyGame

	return render_template('play.html')

@app.route("/game/<gametype>", methods=[ 'GET', 'POST' ])#, methods=[ 'GET', 'POST' ])	# 'GET' and 'POST' are HTML methods that are used in the corresponding html file
def play_game(gametype):
	curruser = session.get('curruser', None) #Get username

	if not curruser:
		return redirect(url_for('index'))

	fileQuestions = easyQuestions

	if gametype == 'medium':
		fileQuestions = mediumQuestions
	elif gametype == 'hard':
		fileQuestions = hardQuestions

	numQuestions = session.get('numQuestions', None)  # Get number of questions
	currentQuestion = session.get('currentQuestion', None)  # Get current question counter
	listOfQuestions = []  # TODO fix this to make questions only able to be asked once
	ret = get_questions(listOfQuestions, fileQuestions, MAXQUESTIONS)
	listOfQuestions.append(ret[5])  # Add used questions
	score = session.get('score', None)  # Get score

	if currentQuestion < numQuestions:
		if request.method == 'GET':
			session['correctAnswer'] = ret[6] # Set correct answer
		if request.method == 'POST':
			correctAnswer = session.get('correctAnswer', None) #Get correct answer
			answer = request.form['answer']  #Get answer from button press

			array = [['A', 'B', 'C', 'D'],[0, 1, 2, 3]] #Array of options and numbers

			if answer is not None and answer in array[0]:
				if correctAnswer == array[1][array[0].index(answer)]:
					score += 10 #Increment on correct
				else:
					score -=5 #Decrement on wrong

			session['correctAnswer'] = ret[6] #Save correct answer
			currentQuestion += 1 #Increment current question
			session['currentQuestion'] = currentQuestion #Save to cookies
			session['score'] = score #Save score
	else:
		correctAnswer = session.get('correctAnswer', None)  # Get correct answer
		answer = request.form['answer']  # Get answer from button press

		array = [['A', 'B', 'C', 'D'], [0, 1, 2, 3]]  # Array of options and numbers

		if answer is not None and answer in array[0]:
			if correctAnswer == array[1][array[0].index(answer)]:
				score += 10  # Increment on correct
			else:
				score -= 5  # Decrement on wrong
		session['score'] = score  # Save score
		return redirect(url_for('gameComplete', gametype=gametype))

	return render_template('quiz.html', question=ret[0], answer1=ret[1], answer2=ret[2], answer3=ret[3],
						answer4=ret[4], score=score, correct=ret[6], currQ=currentQuestion, maxQ=numQuestions, gametype=gametype, currentuser=curruser)

@app.route("/complete/<gametype>", methods=[ 'GET', 'POST' ])#, methods=[ 'GET', 'POST' ])	# 'GET' and 'POST' are HTML methods that are used in the corresponding html file
def gameComplete(gametype):
	curruser = session.get('curruser', None) #Get current user

	if not curruser:
		return redirect(url_for('index'))

	score = session.get('score', None) #Get current score
	session['currentQuestion'] = 1 #Reset current question counter
	message = '' #Message to display on page
	read_from_file() #Reread file to make sure we have updated info
	score = int(score) #Make sure score is an int

	hs = 0 #Set default value
	if curruser in users: #Check in case username doesn't exist somehow
		if gametype == 'easy':
			hs = int(highscoresE[users.index(curruser)])  # Get high score
		elif gametype == 'medium':
			hs = int(highscoresM[users.index(curruser)])  # Get high score
		elif gametype == 'hard':
			hs = int(highscoresH[users.index(curruser)])  # Get high score

	if score > hs:
		message = f'You beat your previous high score of {hs} with a new high score of {score}!' #Set message
		if curruser in users:  # Check in case username doesn't exist somehow
			if gametype == 'easy':
				highscoresE[users.index(curruser)] = score  # Fix score
			elif gametype == 'medium':
				highscoresM[users.index(curruser)] = score  # Fix score
			elif gametype == 'hard':
				highscoresH[users.index(curruser)] = score  # Fix score

			resave_file() #Save file
	elif score == hs:
		message = f'You tied your high score of {hs} points!' #Set message
	elif score < hs:
		message = f'Your score of {score} did not beat your high score of {hs} points :(' #Set message

	return render_template('complete.html', message=message, curruser=curruser) #Render window

if __name__ == "__main__":
	read_from_file()
	port = 5000
	if(len(sys.argv) >= 2):
		port = sys.argv[1]
	#app.secret_key = 'NA.bcr*xB2KJc7W!7mVHeG!xUC9uQo8qAJj7fE7wr2FbHM8A7kdRRaaN7a-zK9*.vxB92o3s.wgLRV76Z6qWvj9gb@Er*2cThNpe'
	app.config['SECRET_KEY'] = 'NA.bcr*xB2KJc7W!7mVHeG!xUC9uQo8qAJj7fE7wr2FbHM8A7kdRRaaN7a-zK9*.vxB92o3s.wgLRV76Z6qWvj9gb@Er*2cThNpe'
	app.run('0.0.0.0', port) # 5000 is the port for the url, change this when test so that multiple devs can run at same time on different ports