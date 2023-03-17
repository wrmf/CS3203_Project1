# Project 1 for CS3203

**Note:** I got the server set up and started the web app. The login and sign-up systems are set up.

## Development

* I'm going to add everyone to the server after spring break. This isn't containerized (for now at least), so it will only run on the server.

### Steps for execution (from within project directory):

1. Use the command `source projectenv/bin/activate` in order to activate the python virtualenv. This is necessary because the python libraries are installed on it.
2. Start the web app with `python app.py`: `app.py` is the main source file for the web app.
	* Within `app.py`, the last line is `app.run('0.0.0.0', 5000)`. **Do not** change the `0.0.0.0`, but the `5000` can be changed to `5001, 5002, 5003, etc.`, and I think this will
	  allow multiple instances of the web app to run at once (for multiple people developing at once).
	* Plan on using `5000` for the main branch
3. To view the web app, type in the URL `http://34.172.253.216:{port number}`. Here, the port number is the `5000...`
	* This will only be viewable when the server and the app are actively running.
