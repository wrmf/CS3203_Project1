import random

def get_easyQuestion(listOfQuestions, questionList):

    num = random.randint(0, len(questionList) - 1)  # Correct answer

    while num in listOfQuestions:  # Make sure this question has not been asked already this game
        num = random.randint(0, len(questionList) - 1)

    listOfAnswers = []
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
    array = []

    while counter < 4:  # Place answers in embed
        if counter == placementOfRightAnswer:  # Place correct answer
            array.append(questionList['Correct'][num])
            counter += 1
        else:  # Place wrong answers
            array.append(questionList['Correct'][listOfAnswers[counterWrongAnswer]])
            counterWrongAnswer += 1
            counter += 1
    return [questionList['Question'][num], array[0], array[1], array[2], array[3], num, placementOfRightAnswer]
