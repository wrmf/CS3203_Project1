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

# Add new score to file
def resave_file():
	afile = open(USERFILE_PATH, 'w')  # Open 'users.txt' to be appended to

	for idx in range(0, len(users)):
		newline = users[idx] + ',' + passwords[idx] + ',' + str(highscores[idx]) + '\n'	# String to be appended to 'users.txt'
		afile.write(newline)  # Append the newline to the end of the file

	afile.close()	# Close file