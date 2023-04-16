import random
import pandas as pd

def get_questions(listOfQuestions, questionList, maxQuestions):

    # iterate through column question len(questionList['Question'])
    #print(f"1: {questionList['Question']} {questionList['Correct']}")

    currentQuestion = random.randint(0, maxQuestions-1)

    while currentQuestion in listOfQuestions:  # Make sure this question has not been asked already this game
        currentQuestion = random.randint(0, maxQuestions-1)


    correctAnswer = currentQuestion * 4

    answersBlock = currentQuestion * 4

    listOfAnswers = []
    counter = 0  # Counter for wrong answer number

    while counter < 3:
        wrongAnswer = random.randint(answersBlock, answersBlock+3)  # Generate location
        if wrongAnswer in listOfAnswers or wrongAnswer == correctAnswer:
            pass  # Do nothing if that answer has already been selected
        else:
            listOfAnswers.append(wrongAnswer)  # Add to list
            counter += 1  # Increment to make sure we only get 3 wrong answers

    placementOfRightAnswer = random.randint(0, 3)  # Randomly generate right answer location
    counterWrongAnswer = 0  # Counter for the number of wrong answers place (for wrong answer array)

    counter = 0  # Reset counter
    array = []
    while counter < 4:  # Place answers in embed
        if counter == placementOfRightAnswer:  # Place correct answer

            array.append(questionList['Correct'][correctAnswer])
            counter += 1

        else:  # Place wrong answers

            array.append(questionList['Correct'][listOfAnswers[counterWrongAnswer]])
            counterWrongAnswer += 1
            counter += 1

    print(f"current question exit: {questionList['Question'][currentQuestion]}")
    return [questionList['Question'][currentQuestion], array[0], array[1], array[2], array[3], currentQuestion, placementOfRightAnswer]
