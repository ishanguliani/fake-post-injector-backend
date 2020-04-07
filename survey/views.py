# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from .models import Question, QuestionNew, ChoiceNew, QuestionPage, QuestionType
from user.models import User
from link.QUESTIONS import QUESTIONS, CHOICE_TEXT_OTHER, OTHER_OPTION_CHOICE_QUESTION_SET, INPUT_TEXT_MULTIPLE_CHOICE_QUESTION_SET, choicesByQuestion
from django.db import transaction, IntegrityError
from collections import defaultdict

def showSurveyLinks(request, id):
    print('entered showSurveyLinks()')
    if not id:
        print('showSurveyLinks(): no id received')
        return

    # get the link object based on user id
    matchingUsers = User.objects.filter(uuid=id)
    if not matchingUsers:
        # backwards compatibility check: new system only compares users based on uuid while older system used pk(id)
        matchingUsers = User.objects.filter(pk=id)
    try:
        currentUser = matchingUsers[0]
    except IndexError:
        print('showSurveyLinks(): user not found')
        return
    print('showSurveyLinks(): success: user details: ', str(currentUser))

    # get the link
    """
    link_text_original = models.CharField(max_length=1000, blank=True)
    link_text_fake = models.CharField(max_length=1000, blank=True)
    link_target_original = models.CharField(max_length=1000, blank=True)
    link_target_fake = models.CharField(max_length=1000, blank=True)
    link_type = models.ForeignKey(LinkType, on_delete=models.SET_NULL, null=True)
    authored_text_original = models.CharField(max_length=1000, blank=True)
    authored_text_fake = models.CharField(max_length=1000, blank=True)
    author_name = models.CharField(max_length=1000, blank=True)
    is_seen = models.BooleanField(default=False)
    is_clicked = models.BooleanField(default=False)
    time_to_view = models.TimeField(blank = True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    """

    allQuestionPages = get_list_or_404(QuestionPage, user=currentUser)
    if not allQuestionPages:
        print('showSurveyLinks(): allQuestionPages not found!')

    print('showSurveyLinks(): success: found ' + str(len(allQuestionPages)) + ' links')
    print("showSurveyLinks: XXX: currentPage : ", str(allQuestionPages[0]))
    print("showSurveyLinks: XXX: questions on this page : total : " + str(len(allQuestionPages[0].questionnew_set.all())))

    return render(request, 'survey/indexLinks.html', {'questionPage': allQuestionPages[0]})

def showSurveyLinksWithPage(request, userId, pageNumber, showAlert = 0):
    """
    :param request:
    :param userId: the user id which is currently taking the survey
    :param pageNumber:  page numbers are 0 indexed
    :return:
    """
    print('entered showSurveyLinksWithPage() with id:', str(userId), "and pageNumber:", str(pageNumber), ", and showAlert: " + str(showAlert))
    if not userId:
        print('showSurveyLinksWithPage(): no id received')
        return

    # get the current user
    matchingUsers = User.objects.filter(uuid=userId)
    if not matchingUsers:
        # backwards compatibility check: new system only compares users based on uuid while older system used pk(id)
        matchingUsers = User.objects.filter(pk=userId)
    currentUser = matchingUsers[0]

    print('showSurveyLinksWithPage(): success: user details: ', str(currentUser))
    # get all the question pages associated with the current user
    allQuestionPages = get_list_or_404(QuestionPage, user=currentUser)
    if not allQuestionPages:
        print('showSurveyLinksWithPage(): allQuestionPages not found!')
        return
    print('showSurveyLinksWithPage(): success: found ' + str(len(allQuestionPages)) + ' pages')
    # check if the page number is a valid one
    if int(pageNumber) < 0 or int(pageNumber) >= len(allQuestionPages):
        print("showSurveyLinksWithPage(): failure: page number is invalid")
        return render(request, 'survey/resultLinks.html')

    # ready to render the current question page
    currentQuestionPage = allQuestionPages[pageNumber]
    print("XXX: showSurveyLinksWithPage: currentPage query set length : " + str(len(currentQuestionPage.questionnew_set.all())))
    print("XXX: showSurveyLinksWithPage: creating questions")

    if len(currentQuestionPage.questionnew_set.all()) <= 0:
        newQuestion1 = QuestionNew(question_text=QUESTIONS[0],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        newQuestion2 = QuestionNew(question_text=QUESTIONS[1],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        newQuestion31 = QuestionNew(question_text=QUESTIONS[21],
                                    question_type=QuestionType.objects.get(question_type=2),
                                    question_page=currentQuestionPage)

        newQuestion32 = QuestionNew(question_text=QUESTIONS[22],
                                    question_type=QuestionType.objects.get(question_type=2),
                                    question_page=currentQuestionPage)

        newQuestion4 = QuestionNew(question_text=QUESTIONS[3],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        newQuestion41 = QuestionNew(question_text=QUESTIONS[31],
                                    question_type=QuestionType.objects.get(question_type=2),
                                    question_page=currentQuestionPage)

        newQuestion5 = QuestionNew(question_text=QUESTIONS[4],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        newQuestion51 = QuestionNew(question_text=QUESTIONS[41],
                                    question_type=QuestionType.objects.get(question_type=2),
                                    question_page=currentQuestionPage)

        newQuestion6 = QuestionNew(question_text=QUESTIONS[5],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        newQuestion7 = QuestionNew(question_text=QUESTIONS[6],
                                   question_type=QuestionType.objects.get(question_type=2),
                                   question_page=currentQuestionPage)

        newQuestion8 = QuestionNew(question_text=QUESTIONS[7],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        try:
            with transaction.atomic():
                newQuestion1.save()
                print("XXX: newQuestion1.save() OK")
                newQuestion2.save()
                print("XXX: newQuestion2.save() OK")
                newQuestion31.save()
                print("XXX: newQuestion31.save() OK")
                newQuestion32.save()
                print("XXX: newQuestion31.save() OK")
                newQuestion4.save()
                print("XXX: newQuestion4.save() OK")
                newQuestion41.save()
                print("XXX: newQuestion41.save() OK")
                newQuestion5.save()
                print("XXX: newQuestion5.save() OK")
                newQuestion51.save()
                print("XXX: newQuestion51.save() OK")
                newQuestion6.save()
                print("XXX: newQuestion6.save() OK")
                newQuestion7.save()
                print("XXX: newQuestion7.save() OK")
                newQuestion8.save()
                print("XXX: newQuestion8.save() OK")
        except IntegrityError:
            print("FAILED1: there has been an error")

        # proceed adding choices to question 1 if not already done
        if len(newQuestion1.choicenew_set.all()) <= 0:
            newChoice11 = ChoiceNew(question=newQuestion1, choice_text=choicesByQuestion[0][0], votes=0, is_selected=False)
            newChoice12 = ChoiceNew(question=newQuestion1, choice_text=choicesByQuestion[0][1], votes=0, is_selected=False)
            newChoice13 = ChoiceNew(question=newQuestion1, choice_text=choicesByQuestion[0][2], votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice11.save()
                    print("XXX: newChoice11.save() OK")
                    newChoice12.save()
                    print("XXX: newChoice12.save() OK")
                    newChoice13.save()
                    print("XXX: newChoice13.save() OK")
            except IntegrityError:
                print("FAILED1: there has been an error")

        # proceed to add choices to question 2 if not already done
        if len(newQuestion2.choicenew_set.all()) <= 0:
            newChoice21 = ChoiceNew(question=newQuestion2, choice_text="Yes", votes=0, is_selected=False)
            newChoice22 = ChoiceNew(question=newQuestion2, choice_text="No", votes=0, is_selected=False)
            newChoice23 = ChoiceNew(question=newQuestion2, choice_text="I am not sure", votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice21.save()
                    print("XXX: newChoice21.save() OK")
                    newChoice22.save()
                    print("XXX: newChoice22.save() OK")
                    newChoice23.save()
                    print("XXX: newChoice23.save() OK")
            except IntegrityError:
                print("FAILED2: there has been an error")

        # proceed to add choices to question 3-1 which is basically an input box type
        if len(newQuestion31.choicenew_set.all()) <= 0:
            newChoice311 = ChoiceNew(question=newQuestion31, choice_text="  ", votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice311.save()
                    print("XXX: newChoice311.save() OK")
            except IntegrityError:
                print("FAILED311: there has been an error")

        # proceed to add choices to question 3-2 which is basically an input box type
        if len(newQuestion32.choicenew_set.all()) <= 0:
            newChoice321 = ChoiceNew(question=newQuestion32, choice_text="  ", votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice321.save()
                    print("XXX: newChoice321.save() OK")
            except IntegrityError:
                print("newChoice321: there has been an error")

        # proceed to add choices to question 4 if not already done
        if len(newQuestion4.choicenew_set.all()) <= 0:
            newChoice41 = ChoiceNew(question=newQuestion4, choice_text=choicesByQuestion[3][0], votes=0, is_selected=False)
            newChoice42 = ChoiceNew(question=newQuestion4, choice_text=choicesByQuestion[3][1], votes=0, is_selected=False)
            newChoice43 = ChoiceNew(question=newQuestion4, choice_text=choicesByQuestion[3][2], votes=0, is_selected=False)
            newChoice44 = ChoiceNew(question=newQuestion4, choice_text=choicesByQuestion[3][3], votes=0, is_selected=False)
            newChoice45 = ChoiceNew(question=newQuestion4, choice_text=choicesByQuestion[3][4], votes=0, is_selected=False)
            newChoice46 = ChoiceNew(question=newQuestion4, choice_text=choicesByQuestion[3][5], votes=0, is_selected=False)
            newChoice47 = ChoiceNew(question=newQuestion4, choice_text=choicesByQuestion[3][6], votes=0, is_selected=False)
            newChoice48 = ChoiceNew(question=newQuestion4, choice_text=CHOICE_TEXT_OTHER, votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice41.save()
                    print("XXX: newChoice41.save() OK")
                    newChoice42.save()
                    print("XXX: newChoice42.save() OK")
                    newChoice43.save()
                    print("XXX: newChoice43.save() OK")
                    newChoice44.save()
                    print("XXX: newChoice44.save() OK")
                    newChoice45.save()
                    print("XXX: newChoice45.save() OK")
                    newChoice46.save()
                    print("XXX: newChoice46.save() OK")
                    newChoice47.save()
                    print("XXX: newChoice47.save() OK")
                    newChoice48.save()
                    print("XXX: newChoice48.save() OK")
            except IntegrityError:
                print("FAILED4: there has been an error")

        # proceed to add choices to question 4-1 which is basically the optional input box if not already done
        if len(newQuestion41.choicenew_set.all()) <= 0:
            newChoice41 = ChoiceNew(question=newQuestion41, choice_text="  ", votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice41.save()
                    print("XXX: newChoice41.save() OK")
            except IntegrityError:
                print("FAILED41: there has been an error")

        # proceed to add choices to question 5 if not already done
        if len(newQuestion5.choicenew_set.all()) <= 0:
            newChoice51 = ChoiceNew(question=newQuestion5, choice_text=choicesByQuestion[4][0], votes=0, is_selected=False)
            newChoice52 = ChoiceNew(question=newQuestion5, choice_text=choicesByQuestion[4][1], votes=0, is_selected=False)
            newChoice53 = ChoiceNew(question=newQuestion5, choice_text=choicesByQuestion[4][2], votes=0, is_selected=False)
            newChoice54 = ChoiceNew(question=newQuestion5, choice_text=choicesByQuestion[4][3], votes=0, is_selected=False)
            newChoice55 = ChoiceNew(question=newQuestion5, choice_text=choicesByQuestion[4][4], votes=0, is_selected=False)
            newChoice56 = ChoiceNew(question=newQuestion5, choice_text=CHOICE_TEXT_OTHER, votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice51.save()
                    print("XXX: newChoice51.save() OK")
                    newChoice52.save()
                    print("XXX: newChoice52.save() OK")
                    newChoice53.save()
                    print("XXX: newChoice53.save() OK")
                    newChoice54.save()
                    print("XXX: newChoice54.save() OK")
                    newChoice55.save()
                    print("XXX: newChoice55.save() OK")
                    newChoice56.save()
                    print("XXX: newChoice56.save() OK")
            except IntegrityError:
                print("FAILED5: there has been an error")

        # proceed to add choices to question 4-1 which is basically the optional input box if not already done
        if len(newQuestion51.choicenew_set.all()) <= 0:
            newChoice51 = ChoiceNew(question=newQuestion51, choice_text="  ", votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice51.save()
                    print("XXX: newChoice51.save() OK")
            except IntegrityError:
                print("FAILED51: there has been an error")

        # proceed to add choices to question 6 if not already done
        if len(newQuestion6.choicenew_set.all()) <= 0:
            newChoice61 = ChoiceNew(question=newQuestion6, choice_text="Multiple times a day", votes=0, is_selected=False)
            newChoice62 = ChoiceNew(question=newQuestion6, choice_text="At least once a day", votes=0, is_selected=False)
            newChoice63 = ChoiceNew(question=newQuestion6, choice_text="At least once a week", votes=0, is_selected=False)
            newChoice64 = ChoiceNew(question=newQuestion6, choice_text="At least once a month", votes=0, is_selected=False)
            newChoice65 = ChoiceNew(question=newQuestion6, choice_text="Less than once a month", votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice61.save()
                    print("XXX: newChoice61.save() OK")
                    newChoice62.save()
                    print("XXX: newChoice62.save() OK")
                    newChoice63.save()
                    print("XXX: newChoice63.save() OK")
                    newChoice64.save()
                    print("XXX: newChoice64.save() OK")
                    newChoice65.save()
                    print("XXX: newChoice65.save() OK")
            except IntegrityError:
                print("FAILED6: there has been an error")

        # proceed to add choices to question 7 which is basically an input box type
        if len(newQuestion7.choicenew_set.all()) <= 0:
            newChoice71 = ChoiceNew(question=newQuestion7, choice_text="  ", votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice71.save()
                    print("XXX: newChoice71.save() OK")
            except IntegrityError:
                print("newChoice71: there has been an error")

        # proceed to add choices to question 6 if not already done
        if len(newQuestion8.choicenew_set.all()) <= 0:
            newChoice81 = ChoiceNew(question=newQuestion8, choice_text="Multiple times a day", votes=0, is_selected=False)
            newChoice82 = ChoiceNew(question=newQuestion8, choice_text="At least once a day", votes=0, is_selected=False)
            newChoice83 = ChoiceNew(question=newQuestion8, choice_text="At least once a week", votes=0, is_selected=False)
            newChoice84 = ChoiceNew(question=newQuestion8, choice_text="At least once a month", votes=0, is_selected=False)
            newChoice85 = ChoiceNew(question=newQuestion8, choice_text="Less than once a month", votes=0, is_selected=False)

        try:
            with transaction.atomic():
                newChoice81.save()
                print("XXX: newChoice81.save() OK")
                newChoice82.save()
                print("XXX: newChoice82.save() OK")
                newChoice83.save()
                print("XXX: newChoice83.save() OK")
                newChoice84.save()
                print("XXX: newChoice84.save() OK")
                newChoice85.save()
                print("XXX: newChoice85.save() OK")
        except IntegrityError:
            print("FAILED6: there has been an error")

    # if this question has already been answered then just go to the next page
    if currentQuestionPage.is_answered:
        print("showSurveyLinksWithPage: redirecting: already answered")
        return HttpResponseRedirect(reverse('showSurveyLinksWithPage', args=(userId, int(pageNumber) + 1, 0)))
    # print("showSurveyLinksWithPage: currentPage : ", str(currentQuestionPage))
    print("showSurveyLinksWithPage: questions on this page : total : " + str(len(currentQuestionPage.questionnew_set.all())))
    return render(request, 'survey/indexLinks.html', {'questionPage': currentQuestionPage, 'pageNumber':pageNumber, 'showAlert': showAlert})

def surveyResults(request, question_id):
    question = get_object_or_404(QuestionNew, pk=question_id)
    return render(request, 'survey/results.html', {'question': question})

def surveyResultsNew(request, question_page_id):
    questionPage = get_object_or_404(QuestionPage, pk=question_page_id)
    return render(request, 'survey/resultsLinks.html', {'question_page': questionPage})

def surveyVote(request, question_id):
    print('entered: surveyVote')
    question = get_object_or_404(QuestionNew, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, ChoiceNew.DoesNotExist):
        # Redisplay the question voting form.
        # return render(request, 'survey/detail.html', {
        return render(request, 'survey/index.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('surveyResults', args=(question.id,)))


"""
Called when the user submits answers to a question page
"""

def extractAndMarkAnswersFromRequest(request, questionPage, q, validChoices, otherChoicesMap):
    """
    For each question from the question page, get the choice selected by the user and log it.
    Here we exclude questions which are answers to @link{CHOICE_TEXT_OTHER in QUESTIONS.py} preceding question types
    """
    if q in OTHER_OPTION_CHOICE_QUESTION_SET or q in list(map( lambda x: x[0], INPUT_TEXT_MULTIPLE_CHOICE_QUESTION_SET)):
        return
    selected_question = questionPage.questionnew_set.get(question_text=QUESTIONS[q])
    selected_choice = selected_question.choicenew_set.get(pk=request.POST['choice_for_question_text_' + QUESTIONS[q]])
    if CHOICE_TEXT_OTHER in selected_choice.choice_text:
        # the user selected the other option for this question
        print("surveyVoteNew(): extractAndLogAnswers(): Found", CHOICE_TEXT_OTHER, "selected for Question", str(q + 1), ": ", selected_question)
        otherChoicesMap[q] = True
    selected_choice.is_selected = True
    selected_choice.votes += 1
    print("surveyVoteNew(): extractAndLogAnswers(): Question", str(q + 1), ": ", selected_question)
    print("surveyVoteNew(): extractAndLogAnswers(): len(selected_question.choicenew_set)", str(q + 1), ": ", len(selected_question.choicenew_set.all()))
    print("surveyVoteNew(): extractAndLogAnswers(): Choice", str(q + 1), ": ", selected_choice)
    validChoices.append(selected_choice)
    print("surveyVoteNew(): extractAndLogAnswers(): appended as valid choice!")

def surveyVoteNew(request, question_page_id, page_number):
    """
    This is triggered when the user submits a survey question page
    request:            incoming request
    question_page_id:   the page id of the submitted question page
    page_number:        of the submitted page
    """
    print('surveyVoteNew(): entered with question_page_id: ' + str(question_page_id) + ", pageNumber: " + str(page_number))
    for querySet in request.POST:
        print(querySet, ':', request.POST[querySet])
    questionPage = get_object_or_404(QuestionPage, pk=question_page_id)

    currentUserUuId = questionPage.user.uuid
    print('surveyVoteNew(): extracted user uuid: ' + str(currentUserUuId))
    try:
        validChoices = []
        otherChoicesMap = defaultdict(bool)
        for sno in QUESTIONS:
            extractAndMarkAnswersFromRequest(request, questionPage, sno, validChoices, otherChoicesMap)
        print("surveyVoteNew(): otherChoiceMap: " + str(otherChoicesMap))
        # extract the specified text from the input box of the following question of each question
        # where the user selected the @{CHOICE_TEXT}(Other) as the answer
        for questionWithOtherOptionSelected in otherChoicesMap:
            questionKeyWhichContainsTextForOtherOption = questionWithOtherOptionSelected * 10 + 1  # 2 -> 2*10 + 1 = 21, 3 -> 3*10 + 1 = 31, 6 = 6*10 + 1 = 61
            questionObject = questionPage.questionnew_set.get(question_text=QUESTIONS[questionKeyWhichContainsTextForOtherOption])
            selectedChoice = questionObject.choicenew_set.all()[0]
            choiceText = request.POST['choice_for_question_text_' + QUESTIONS[questionKeyWhichContainsTextForOtherOption]]
            if not choiceText.strip():
                raise KeyError('surveyVoteNew(): otherChoiceOption: no text specified for question: ' + str(QUESTIONS[questionKeyWhichContainsTextForOtherOption]))
            # at this point if the above key is not found in the request then this means that the user did select the Other option
            # for the question but did not type in any text against it. This will throw a KeyError and we will not proceed with saving these choices
            print("surveyVoteNew(): otherChoiceOption: Question:", str(questionObject))
            print("surveyVoteNew(): otherChoiceOption: SelectedChoice:", str(selectedChoice))
            print("surveyVoteNew(): otherChoiceOption: ChoiceText:", choiceText)
            selectedChoice.choice_text = choiceText
            selectedChoice.is_selected = True
            selectedChoice.votes += 1
            validChoices.append(selectedChoice)

        for questionNumberWithInputText, regexPattern in INPUT_TEXT_MULTIPLE_CHOICE_QUESTION_SET:
            questionObject = questionPage.questionnew_set.get(question_text=QUESTIONS[questionNumberWithInputText])
            selectedChoice = questionObject.choicenew_set.all()[0]
            for key in request.POST:
                print("looking into key: ", str(key))
                # hack: there was some problem while directly extracting results from the incoming POST request by using
                # request.POST['choice_for_question_text_' + questions[questionNumberWithInputText]] as the key. It seems to be that this happens
                # because the question at that index is actually a long string with some special characters and utf-8 messes things up somewhere
                # the current solution is to only match the most relevant part of the first line of the question over matchihng the
                # whole question string.
                if regexPattern in key:
                    choiceText = "NA"
                    try:
                        choiceText = str(request.POST[key])
                    except:
                        pass
                    # choiceText = str(request.POST['choice_for_question_text_' + questions[questionNumberWithInputText]])
                    # parse comma separated choices to remove white spaces
                    # parse input choices to remove starting and trailing white spaces
                    # for example for input "1, 2, 3  , this is my selected option   " we should remove the starting and trailing white space for each selection
                    # this will become: "1,2,3,this is my selected option"
                    parsedChoiceText = ""
                    for choice in choiceText.strip().split(","):
                        parsedChoiceText += choice.strip() + ','
                    print("surveyVoteNew(): questionStringWithInputText: Question:", str(QUESTIONS[questionNumberWithInputText]))
                    print("surveyVoteNew(): questionStringWithInputText: SelectedChoice:", str(selectedChoice))
                    print("surveyVoteNew(): questionStringWithInputText: ChoiceText:", parsedChoiceText)
                    selectedChoice.choice_text = parsedChoiceText
                    selectedChoice.is_selected = True
                    selectedChoice.votes += 1
                    validChoices.append(selectedChoice)

        # save all requests to db since none of them caused an error
        for sno, selected_choice in enumerate(validChoices):
            selected_choice.save()
            print("surveyVoteNew(): success: saved choice: ", selected_choice, ': ')

        # update the is_clicked field for the corresponding link model
        try:
            # the idea is to extract the first matching choice from the list of valid choices whose question text matches the question "Did you click on this link" i.e value of QUESTIONS[0]
            choiceForDidYouClickOnThisLink = list(filter( lambda choiceObject: choiceObject.question.question_text == QUESTIONS[0], validChoices))[0]
            selectedChoiceText = str(choiceForDidYouClickOnThisLink.choice_text)
            print("surveyVoteNew(): choiceForDidYouClickOnThisLink: ", selectedChoiceText)
            if choicesByQuestion[0][0] in selectedChoiceText:
                print("surveyVoteNew(): choiceForDidYouClickOnThisLink: The link was clicked!")
                questionPage.link_model.is_clicked = True
            else:
                print("surveyVoteNew(): choiceForDidYouClickOnThisLink: The link was NOT clicked!")
                questionPage.link_model.is_clicked = False
            questionPage.link_model.save()
        except:
            print("surveyVoteNew(): choiceForDidYouClickOnThisLink: could not be extracted. Something went wrong.")


    except (KeyError, ChoiceNew.DoesNotExist):
        # Redisplay the questionPage voting form.
        print("surveyVoteNew(): failure: something went wrong in selecting choice")
        return HttpResponseRedirect(reverse('showSurveyLinksWithPage', args=(currentUserUuId, int(page_number), 1)))
    else:
        # time to save this QuestionPage with all the answered questions
        # if the user selected YES to the question "Did you click on this link ?"
        # then mark the corresponding link model is_clicked field to True
        # if selected_choice4.choice_text.lower().strip() == "yes".strip():
        #     print("surveyVoteNew(): This is a YES")
        #     questionPage.link_model.is_clicked = True
        #     # save this change
        #     questionPage.link_model.save()
        questionPage.is_answered = True
        questionPage.save()
        print("surveyVoteNew(): success!: saved question page")

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # return HttpResponseRedirect(reverse('surveyResultsNew', args=(questionPage.id,)))
        # pass the next page
        # return HttpResponseRedirect(reverse('showSurveyLinksWithPage', args=(questionPage.id, int(pageNumber)+1)))
        return HttpResponseRedirect(reverse('showSurveyLinksWithPage', args=(currentUserUuId, int(page_number) + 1, 0)))

def surveyVoteNewBypass(request, question_page_id, page_number, bypass):
    print('surveyVoteNew(): entered with question_page_id: ' + str(question_page_id) + ", pageNumber: " + str(page_number))
    print(request.POST)
    questionPage = get_object_or_404(QuestionPage, pk=question_page_id)
    currentUserId = questionPage.user.uuid
    return HttpResponseRedirect(reverse('showSurveyLinksWithPage', args=(currentUserId, int(page_number) + 1, 0)))
