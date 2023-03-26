# Project 1 for CS3203

## Steps for execution (from within project directory):

**Note:** Any instance of using the command `python` may require the use of `python3` depending on the machine its running on.

1. Execute 	`pip install -r requirements.txt` to get all dependencies
3. Start the web app with `python app.py`: `app.py` is the main source file for the web app.
	* Can also use `python app.py {port}` where `{port}` is the desired port number. The port will default to **5000** if not specified
	* Within `app.py`, the last line is `app.run('0.0.0.0', port)`. **Do not change this**. This lets the app run on localhost with the specified port.
4. To view the web app, type in the URL `http://127.0.0.1:{port}` (if running on your local machine).
	* For the server (if it is running), the URL will be `http://34.172.253.216:{port}`
