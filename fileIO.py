import pandas as pd

USERFILE_PATH = 'static/users.csv'	# 'users.txt' path
users = []; passwords = []; highscoresE = []; highscoresM = []; highscoresH = []	# Declare lists for users, passwords, and highscores
user_df = pd.read_csv(USERFILE_PATH)

# Read usernames, passwords, and highscores from 'users.csv' file, then add them to the lists
def read_from_file():
	user_df = pd.read_csv(USERFILE_PATH)
	user_df.reset_index()
	users.clear(); passwords.clear(); highscoresE.clear(); highscoresM.clear(); highscoresH.clear()
	for index, row in user_df.iterrows():
		users.append(row['Username'])
		passwords.append(row['Password'])
		highscoresE.append(row['HSE'])
		highscoresM.append(row['HSM'])
		highscoresH.append(row['HSH'])

# Append a line to the end of 'users.csv'
def append_to_file():
	idx = len(users) - 1
	user_df.loc[len(user_df.index)] = [users[idx], passwords[idx], highscoresE[idx], highscoresM[idx], highscoresH[idx]]  	# Add row to end of df
	user_df.to_csv(USERFILE_PATH, index = False)	# Write dataframe to .csv file

# Rewrite the whole csv with any new values
def resave_file():
	# Make new dataframe with new values
	temp_df = pd.DataFrame(list(zip(users, passwords, highscoresE, highscoresM, highscoresH)), columns=['Username', 'Password', 'HSE', 'HSM', 'HSH'])
	user_df = temp_df	# Replace old dataframe with new values
	user_df.to_csv(USERFILE_PATH, index = False)	# Save as .csv
