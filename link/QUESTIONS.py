# old questions
# questions = ['What is the topic of the post?', 'What is your relationship with the author?',  'Why do you find this post interesting?', 'Did you click on this post?']
ADDITIONAL_INSTRUCTIONS_FOR_MULTIPLE_CHOICE_QUESTIONS = '\nNOTE: Please enter your answers separated by commas. For `Other` option, add your response at the end.\nFor example: If your answer is option a, option c and Other then please write: a,c,this my answer to this question'
# new questions
questions = {0: 'Did you click on this link?' # Question 1
    , 1: 'Does the author usually share posts like this?' # Question 2
    , 21: "Why did you click on this link? Please select all that apply. \n "
          "a. The content/preview looks interesting \n "
          "b. I would like to discuss with the post author about the content in the link at a later time \n "
          "c. The author doesn't usually share this kind of content in social network \n "
          "d. Other, please specify\n "
          "" + ADDITIONAL_INSTRUCTIONS_FOR_MULTIPLE_CHOICE_QUESTIONS   # Question 31 - Others
    , 22: "Why did you not click on this link? Please select all that apply. \n "
          "a. The author doesn't usually share this kind of content in social network \n "
          "b. The content/preview of the link is not relevant to my interest \n "
          "c. I do not think, the shared link is authentic \n "
          "d. Other\n "
          "" + ADDITIONAL_INSTRUCTIONS_FOR_MULTIPLE_CHOICE_QUESTIONS # Question 32 - Others
    , 3: 'How do you describe your relationship with this person?'  # Question 4
    , 31: "Specify relationship below if you selected 'Others' above"  # Question 41 - Others
    , 4: 'What is the topic of the post?' # Question 5
    , 41: "Specify topic below if you selected 'Others' above"  # Question 51 - Others
    , 5: 'How frequently do you notice this person sharing a post similar to this?' # Question 6
    , 6: 'What types of posts does this person generally share? Select all that apply.\n '
         'a. Sales-oriented (e.g. clothes sales, modeling opportunities)\n '
         'b. Media (e.g. videos, pictures)\n '
         'c. Interactives (e.g. quizzes, games)\n '
         'd. Other\n '
         '' + ADDITIONAL_INSTRUCTIONS_FOR_MULTIPLE_CHOICE_QUESTIONS # Question 7
    , 7: 'How frequently do you click on a post shared by this person?' # Question 8
    }

# the following questions will be exclude from choice extraction process
# since they have the "Others" option in them
OTHER_OPTION_CHOICE_QUESTION_SET = set()
OTHER_OPTION_CHOICE_QUESTION_SET.add(31)
OTHER_OPTION_CHOICE_QUESTION_SET.add(41)

# the following questions are of input type and hence will have their choice
# directly extracted from the incoming POST request
INPUT_TEXT_MULTIPLE_CHOICE_QUESTION_SET = set()
INPUT_TEXT_MULTIPLE_CHOICE_QUESTION_SET.add((21, "Why did you click on this link?"))
INPUT_TEXT_MULTIPLE_CHOICE_QUESTION_SET.add((22, "Why did you not click on this link?"))
INPUT_TEXT_MULTIPLE_CHOICE_QUESTION_SET.add((6, "What types of posts does this person generally share"))

CHOICE_TEXT = 'Other'

