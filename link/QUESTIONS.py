# old questions
# questions = ['What is the topic of the post?', 'What is your relationship with the author?',  'Why do you find this post interesting?', 'Did you click on this post?']
# new questions
questions = {0: 'Did you click on this link?' # Question 1
    , 1: 'Does the author usually share posts like this?' # Question 2
    , 2: 'Why did you click or not click on this link?' # Question 3
    , 21: "Specify reason below if you selected 'Others' above"  # Question 31 - Others
    , 3: 'How do you describe your relationship with this person?'  # Question 4
    , 31: "Specify relationship below if you selected 'Others' above"  # Question 41 - Others
    , 4: 'What is the topic of the post?' # Question 5
    , 41: "Specify topic below if you selected 'Others' above"  # Question 51 - Others
    , 5: 'How frequently do you notice this person sharing a post similar to this?' # Question 6
    , 6: 'What types of posts does this person generally share? [For this question, participant should be able to choose multiple options]' # Question 7
    , 61: "Specify post types below if you selected 'Others' above"  # Question 61 - Others
    , 7: 'How frequently do you click on a post shared by this person?' # Question 8
    }


CHOICE_TEXT = 'Other(please specify):'

def doSomething(i, mMap):
    mMap[i] = chr(65 + i)

def doSomethingWithList(i, l):
    l.append(i+1)

from collections import defaultdict

d = defaultdict(bool);
for i in range(5):
    print(d[i])

