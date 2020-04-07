# old questions
# questions = ['What is the topic of the post?', 'What is your relationship with the author?',  'Why do you find this post interesting?', 'Did you click on this post?']
CHOICE_TEXT_OTHER = 'Other'
ADDITIONAL_INSTRUCTIONS_FOR_MULTIPLE_CHOICE_QUESTIONS = "\nNOTE: Please enter your answers separated by commas. For `" + CHOICE_TEXT_OTHER + "` option, add your response at the end.\nFor example: If your answer is option a, option c and " + CHOICE_TEXT_OTHER + " then please write: a,c,this my answer to this question"
# new questions
QUESTIONS = {0: 'Did you click on this link?'  # Question 1
    , 1: 'Does this account usually share posts like this?'  # Question 2
    , 21: "Why did you click on this link? Please select all that apply. \n "
          "a. The content/preview looks interesting \n "
          "b. I would like to discuss with the post author about the content in the link at a later time \n "
          "c. The author doesn't usually share this kind of content in social network \n "
          "d. " + CHOICE_TEXT_OTHER + ", please specify\n "
          "" + ADDITIONAL_INSTRUCTIONS_FOR_MULTIPLE_CHOICE_QUESTIONS  # Question 31 - Others
    , 22: "Why did you NOT click on this link? Please select all that apply. \n "
          "a. The author doesn't usually share this kind of content in social network \n "
          "b. The content/preview of the link is not relevant to my interest \n "
          "c. I do not think the shared link is authentic \n "
          "d. " + CHOICE_TEXT_OTHER + "\n "
          "" + ADDITIONAL_INSTRUCTIONS_FOR_MULTIPLE_CHOICE_QUESTIONS  # Question 32 - Others
    , 3: 'How do you describe your relationship with this account?'  # Question 4
    , 31: "Specify relationship below if you selected 'Others' above"  # Question 41 - Others
    , 4: 'What is the topic of the post?'  # Question 5
    , 41: "Specify topic below if you selected 'Others' above"  # Question 51 - Others
    , 5: 'How frequently do you notice this account sharing a post similar to this?'  # Question 6
    , 6: 'What types of posts does this account generally share? Select all that apply.\n '
         'a. Sales-oriented (e.g. clothes sales, modeling opportunities)\n '
         'b. Media (e.g. videos, pictures)\n '
         'c. Interactives (e.g. quizzes, games)\n '
         'd. Informatives (e.g. news, listicles)\n '
         'e. Personal updates\n '
         "f. " + CHOICE_TEXT_OTHER + "\n "
         '' + ADDITIONAL_INSTRUCTIONS_FOR_MULTIPLE_CHOICE_QUESTIONS  # Question 7
    , 7: 'How frequently do you click on a post shared by this account?'  # Question 8
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

choicesByQuestion = {
    0:['Yes (if you choose this option, skip question #4)',
       'No (if you choose this option, skip question #3)',
       'I am not sure (if you choose this option, skip question #3 & #4)',
       ],
    3:['Spouse/Partner/Boyfriend/Girlfriend',
       'Close friend',
       'Family',
       'Co-worker/classmate',
       'Acquaintance',
       'Public page',
       'Sponsored post',
       ],
    4:['Sales-oriented (e.g. clothes sales, modeling opportunities)',
       'Media (e.g. videos, pictures)',
       'Interactives (e.g. quizzes, games)',
       'Informatives (e.g. news, listicles)',
       'Personal updates',
       ],
}


