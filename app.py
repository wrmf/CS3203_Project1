from flask import Flask, render_template, request, redirect, url_for, session
import sys
from modules.questions import *
from fileIO import *
import pandas as pd

TEMPLATES_AUTO_RELOAD = True

MAXQUESTIONS = 5
MINQUESTIONS = 2

# Flask Web App
app = Flask(__name__)

easyQuestions = pd.read_csv('static/easyQuestions.csv')

# index page
@app.route("/", methods=[ 'GET', 'POST' ])	# 'GET' and 'POST' are HTML methods that are used in the corresponding html file
def index():
	read_from_file()	# Initalize lists
	return render_template('index.html', error=None)

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
			if (password == confirm):	# Check that the entered password and the re-entered passwords match
				# Add the username, password, and highscore to their respective lists
				users.append(username)
				passwords.append(password)
				highscores.append(0)
				append_to_file()	# Add the new user with their password and 0 highscore to the end of 'users.txt'
				session['curruser'] = username
				return redirect(url_for('home'))	# If successful, go to the home page and pass user index
			else:	# Throw error if passwords don't match
				error = 'Passwords do not match'

	return render_template('sign-up.html', error=error)

# home page
@app.route("/home/", methods=[ 'GET', 'POST' ])
def home():
	error = None
	curruser = session.get('curruser', None)

	# If there is no user logged in, render index and throw error
	if not curruser:
		error = 'Currently not logged in'
		return render_template('index.html', error=error)

	if request.method == 'POST':
		if request.form.get('ind') == 'Logout':  # Logout button (send to index)
			session.pop('curruser')	# Logout user
			return redirect(url_for('index')) #redirect to main page
		if request.form.get('play') == 'play':  # Check if 'play' was hit
			return redirect(url_for('play')) #redirect to play page

	return render_template('home.html', currentuser = curruser)

# home page
@app.route("/play/", methods=[ 'GET', 'POST' ])
def play():
	global numQuestions #get number of questions
	curruser = session.get('curruser', None)

	if request.method == 'POST':
		if request.form.get('go') == 'GO!':  # This is a login button to take users to the login page
			numQ = int(request.form['numQ'])	# Get username
			if numQ < MINQUESTIONS: #Check if number input was less than minimum
				numQuestions = MINQUESTIONS
			elif numQ > MAXQUESTIONS: #Check if number input was more than maximum
				numQuestions = MAXQUESTIONS
			else:
				numQuestions = numQ #Set number of questions to ask
			session['numQuestions'] = numQuestions #Save to session
			session['currentQuestion'] = 1 #reset current question counter
			session['score'] = 0 #Reset score
			return redirect(url_for('play_easyGame')) #Redirect to /easyGame

	return render_template('play.html')

@app.route("/easyGame/", methods=[ 'GET', 'POST' ])#, methods=[ 'GET', 'POST' ])	# 'GET' and 'POST' are HTML methods that are used in the corresponding html file
def play_easyGame():
	curruser = session.get('curruser', None) #Get username
	numQuestions = session.get('numQuestions', None) #Get number of questions
	currentQuestion = session.get('currentQuestion', None) #Get current question counter
	listOfQuestions = [] #TODO fix this to make questions only able to be asked once
	ret = get_easyQuestion(listOfQuestions, easyQuestions)
	listOfQuestions.append(ret[5]) #Add used questions
	score = session.get('score', None) #Get score

	if currentQuestion < numQuestions:
		if request.method == 'GET':
			session['correctAnswer'] = ret[6] #Set correct answer
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
		return redirect(url_for('gameComplete'))


	return render_template('easyquiz.html', question=ret[0], answer1=ret[1], answer2=ret[2], answer3=ret[3],
						answer4=ret[4], score=score, correct=ret[6], currQ=currentQuestion, maxQ=numQuestions)

@app.route("/complete/", methods=[ 'GET', 'POST' ])#, methods=[ 'GET', 'POST' ])	# 'GET' and 'POST' are HTML methods that are used in the corresponding html file
def gameComplete():
	curruser = session.get('curruser', None) #Get current user
	score = session.get('score', None) #Get current score
	session['currentQuestion'] = 1 #Reset current question counter
	message = '' #Message to display on page
	read_from_file() #Reread file to make sure we have updated info
	score = int(score) #Make sure score is an int

	hs = 0 #Set default value
	if curruser in users: #Check in case username doesn't exist somehow
		hs = int(highscores[users.index(curruser)])  # Get high score

	if score > hs:
		message = f'You beat your previous high score of {hs} with a new high score of {score}!' #Set message
		if curruser in users:  # Check in case username doesn't exist somehow
			highscores[users.index(curruser)] = score #Fix score
			resave_file() #Save file
	elif score == hs:
		message = f'You tied your high score of {hs} points!' #Set message
	elif score < hs:
		message = f'Your score of {score} did not beat your high score of {hs} points :(' #Set message

	return render_template('complete.html', message=message, curruser=curruser) #Render window

if __name__ == "__main__":
	port = 5000
	if(len(sys.argv) >= 2):
		port = sys.argv[1]
	#app.secret_key = 'NA.bcr*xB2KJc7W!7mVHeG!xUC9uQo8qAJj7fE7wr2FbHM8A7kdRRaaN7a-zK9*.vxB92o3s.wgLRV76Z6qWvj9gb@Er*2cThNpe'
	app.config['SECRET_KEY'] = 'NA.bcr*xB2KJc7W!7mVHeG!xUC9uQo8qAJj7fE7wr2FbHM8A7kdRRaaN7a-zK9*.vxB92o3s.wgLRV76Z6qWvj9gb@Er*2cThNpe'
	app.run('0.0.0.0', port)	# 5000 is the port for the url, change this when test so that multiple devs can run at same time on different ports
