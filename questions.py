import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

@app.route("/easyGame", methods=[ 'GET', 'POST' ])	# 'GET' and 'POST' are HTML methods that are used in the corresponding html file
def play_easyGame(numQuestions = 5):

    questionList = pd.read_csv('static/easyQuestions.csv')
    listOfQuestions = []
    numQuestionCounter = 0

    while numQuestionCounter < numQuestions:  # Multiple questions

        num = random.randint(0, len(question) - 1)  # Correct answer

        while num in listOfQuestions:  # Make sure this question has not been asked already this game
            num = random.randint(0, len(questionList) - 1)
        listOfQuestions.append(num)  # Add answer

        listOfAnswers = []  # Wrong answer array
        counter = 0  # Counter for wrong answer number

        while counter < 3:
            num2 = random.randint(0, (len(questionList) - 1))  # Generate location
            if num2 in listOfAnswers or num2 == num:
                pass  # Do nothing if that answer has already been selected
            else:
                listOfAnswers.append(num2)  # Add to list
                counter += 1  # Increment to make sure we only get 3 wrong answers

        placementOfRightAnswer = random.randint(0, 3)  # Randomly generate right answer location
        counterWrongAnswer = 0  # Counter for the number of wrong answers place (for wrong answer array)

        counter = 0  # Reset counter

        while counter < 4:  # Place answers in embed
            if counter == placementOfRightAnswer:  # Place correct answer

                counter += 1
            else:  # Place wrong answers

                counterWrongAnswer += 1
                counter += 1
        return render_template('easyquiz.html', currentuser=curruser)

