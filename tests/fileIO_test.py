from fileIO import *

def test_read():
    read_from_file()

    # Append data to lists
    users.append('testread')
    passwords.append('testread')
    highscoresE.append(0); highscoresM.append(0); highscoresH.append(0)

    # Show that once read_from_file is called, 'testread' is no longer in lists
    read_from_file()
    assert 'testread' not in users
    assert 'testread' not in passwords

    # Test that 'test' is a username in the file
    assert 'test' in users


def test_append():
    # Append to lists
    read_from_file()
    users.append('testappend')
    passwords.append('testappend')
    highscoresE.append(0); highscoresM.append(0); highscoresH.append(0)

    # Append to file
    append_to_file()

    # Test if in file
    # Clear lists just in case
    users.clear(); passwords.clear(); highscoresE.clear(); highscoresM.clear(); highscoresH.clear()
    read_from_file()
    # Check that new user is at the end of the file
    assert users[-1] == 'testappend'
    assert passwords[-1] == 'testappend'


def test_resave():
    read_from_file()
    idx = users.index('test')  # Get the index of 'test'

    passwords[idx] = 'savetest'  # Change the password for user 'test'
    highscoresE[idx] = 1101011100011010  # Change easy high score of user 'test'
    resave_file()  # Save

    # Test that new password and highscore are in file at correct index
    users.clear(); passwords.clear(); highscoresE.clear(); highscoresM.clear(); highscoresH.clear()
    read_from_file()
    assert passwords[idx] == 'savetest'
    assert highscoresE[idx] == 1101011100011010
