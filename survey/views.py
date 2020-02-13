# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from .models import Question, QuestionNew, ChoiceNew, QuestionPage, QuestionType
from user.models import User
from link.QUESTIONS import questions, CHOICE_TEXT
from django.db import transaction, IntegrityError
from collections import defaultdict
from link.models import LinkModel
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

#
# def showSurveyView(ListView):
#     template_name = 'survey/index.html'
#     context_object_name = 'latest_question_list'
#     def get_queryset(self):
#         return Question.objects.all()

# def showSurvey(request):
#     # return render(request, "survey/surveyForm.html", {'form': SurveyModelForm()})
#     # XXX
#     # latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     latest_question_list = QuestionNew.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'survey/index.html', context)
def showSurveyLinks(request, id):
    print('entered showSurveyLinks()')
    if not id:
        print('showSurveyLinks(): no id received')
        return

    # get the link object based on user id
    currentUser = User.objects.filter(pk=id)[0]
    if not currentUser:
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

    # allLinks = get_list_or_404(LinkModel, user=currentUser)
    # if not allLinks:
    #     print('showSurveyLinks(): allLinks not found!')
    # print('showSurveyLinks(): success: found ' + str(len(allLinks)) + ' links')

    allQuestionPages = get_list_or_404(QuestionPage, user=currentUser)
    if not allQuestionPages:
        print('showSurveyLinks(): allQuestionPages not found!')

    print('showSurveyLinks(): success: found ' + str(len(allQuestionPages)) + ' links')

    # XXX
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # latest_question_list = QuestionNew.objects.order_by('-pub_date')[:5]

    # XXX adding all the links one by one to QuestionPage model
    # questionPageList = []
    # for link in allLinks:
    #     # create a new question page and add to question page list
    #     newQuestionPage = QuestionPage(user=currentUser, link_model=link)
    #     # save this question page
    #     newQuestionPage.save()
    #     print("XXX: created new page: " + str(newQuestionPage))
    #     questionPageList.append(newQuestionPage)

    # print("XXX: total ", str(len(questionPageList)))
    # questionList = []
    # print('questionList: length: ', len(questionList))
    # for link in allLinks:
    #     questionSet = []
    #     for question in latest_question_list:
    #         # bind each question to the single link
    #         question.link_model = link
    #         # bind each question to a particular user
    #         question.user = currentUser
    #         questionSet.append(question)
    #     print('questionList: questionSet: appended question: length: ', len(questionSet))
    #     questionList.append(questionSet)
    #     print('questionList: appended questionSet, length: ', len(questionList))
    #
    # latest_question_list = questionList

    # return render(request, 'survey/indexLinks.html',
    #               {'allLinks': allLinks, 'latest_question_list': latest_question_list})
    print("showSurveyLinks: XXX: currentPage : ", str(allQuestionPages[0]))
    print("showSurveyLinks: XXX: questions on this page : total : " + str(len(allQuestionPages[0].questionnew_set.all())))
    # for i, choice in enumerate(allQuestionPages[0].questionnew_set.objects.all()):
    #     print("XXX: choice", i, ": ", choice)

    return render(request, 'survey/indexLinks.html', {'questionPage': allQuestionPages[0]})

    # return render(request, 'survey/indexLinks.html', {'allLinks': allLinks, 'latest_question_list': latest_question_list})

"""
Called to load a new survey question page
"""
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
    currentUser = User.objects.filter(pk=userId)[0]
    if not currentUser:
        print('showSurveyLinksWithPage(): user not found')
        return
    print('showSurveyLinksWithPage(): success: user details: ', str(currentUser))
    # get all the question pages associated with the current user
    allQuestionPages = get_list_or_404(QuestionPage, user=currentUser)
    if not allQuestionPages:
        print('showSurveyLinksWithPage(): allQuestionPages not found!')
        return
    print('showSurveyLinksWithPage(): success: found ' + str(len(allQuestionPages)) + ' pages')
    # check if the page number is a valid one
    if  int(pageNumber) < 0 or int(pageNumber) >= len(allQuestionPages):
        print("showSurveyLinksWithPage(): failure: page number is invalid")
        return render(request, 'survey/resultLinks.html')

    # ready to render the current question page
    currentQuestionPage = allQuestionPages[pageNumber]
    print("XXX: showSurveyLinksWithPage: currentPage query set length : " + str(len(currentQuestionPage.questionnew_set.all())))
    print("XXX: showSurveyLinksWithPage: creating questions")

    if len(currentQuestionPage.questionnew_set.all()) <= 0:
        newQuestion1 = QuestionNew(question_text=questions[0],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        newQuestion2 = QuestionNew(question_text=questions[1],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        newQuestion3 = QuestionNew(question_text=questions[2],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        newQuestion31 = QuestionNew(question_text=questions[21],
                                   question_type=QuestionType.objects.get(question_type=2),
                                   question_page=currentQuestionPage)

        newQuestion4 = QuestionNew(question_text=questions[3],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        newQuestion41 = QuestionNew(question_text=questions[31],
                                    question_type=QuestionType.objects.get(question_type=2),
                                    question_page=currentQuestionPage)

        newQuestion5 = QuestionNew(question_text=questions[4],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        newQuestion51 = QuestionNew(question_text=questions[41],
                                    question_type=QuestionType.objects.get(question_type=2),
                                    question_page=currentQuestionPage)

        newQuestion6 = QuestionNew(question_text=questions[5],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        newQuestion7 = QuestionNew(question_text=questions[6],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        newQuestion71 = QuestionNew(question_text=questions[61],
                                    question_type=QuestionType.objects.get(question_type=2),
                                    question_page=currentQuestionPage)

        newQuestion8 = QuestionNew(question_text=questions[7],
                                   question_type=QuestionType.objects.get(question_type=1),
                                   question_page=currentQuestionPage)

        try:
            with transaction.atomic():
                newQuestion1.save()
                print("XXX: newQuestion1.save() OK")
                newQuestion2.save()
                print("XXX: newQuestion2.save() OK")
                newQuestion3.save()
                print("XXX: newQuestion3.save() OK")
                newQuestion31.save()
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
                newQuestion71.save()
                print("XXX: newQuestion71.save() OK")
                newQuestion8.save()
                print("XXX: newQuestion8.save() OK")
        except IntegrityError:
            print("FAILED1: there has been an error")

        # proceed adding choices to question 1 if not already done
        if len(newQuestion1.choicenew_set.all()) <= 0:
            newChoice11 = ChoiceNew(question=newQuestion1, choice_text="Yes", votes=0, is_selected=False)
            newChoice12 = ChoiceNew(question=newQuestion1, choice_text="No", votes=0, is_selected=False)
            newChoice13 = ChoiceNew(question=newQuestion1, choice_text="I am not sure", votes=0, is_selected=False)

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


        # proceed to add choices to question 3 if not already done
        if len(newQuestion3.choicenew_set.all()) <= 0:
            newChoice31 = ChoiceNew(question=newQuestion3, choice_text="The topic is interesting", votes=0, is_selected=False)
            newChoice32 = ChoiceNew(question=newQuestion3, choice_text="I would like to discuss with the post author about the link later", votes=0, is_selected=False)
            newChoice33 = ChoiceNew(question=newQuestion3, choice_text=CHOICE_TEXT, votes=0, is_selected=False)
            # newChoice31 = ChoiceNew(question=newQuestion3, choice_text="  ", votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice31.save()
                    print("XXX: newChoice31.save() OK")
                    newChoice32.save()
                    print("XXX: newChoice32.save() OK")
                    newChoice33.save()
                    print("XXX: newChoice33.save() OK")
            except IntegrityError:
                print("FAILED3: there has been an error")

        # proceed to add choices to question 4-1 which is basically the optional input box if not already done
        if len(newQuestion31.choicenew_set.all()) <= 0:
            newChoice31 = ChoiceNew(question=newQuestion31, choice_text="  ", votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice31.save()
                    print("XXX: newChoice31.save() OK")
            except IntegrityError:
                print("FAILED31: there has been an error")

        # proceed to add choices to question 4 if not already done
        if len(newQuestion4.choicenew_set.all()) <= 0:
            newChoice41 = ChoiceNew(question=newQuestion4, choice_text="Spouse/Partner/Boyfriend/Girlfriend", votes=0, is_selected=False)
            newChoice42 = ChoiceNew(question=newQuestion4, choice_text="Close friend", votes=0, is_selected=False)
            newChoice43 = ChoiceNew(question=newQuestion4, choice_text="Acquaintance", votes=0, is_selected=False)
            newChoice44 = ChoiceNew(question=newQuestion4, choice_text="Public page", votes=0, is_selected=False)
            newChoice45 = ChoiceNew(question=newQuestion4, choice_text=CHOICE_TEXT, votes=0, is_selected=False)
            # newChoice41 = ChoiceNew(question=newQuestion4, choice_text="Yes", votes=0, is_selected=False)
            # newChoice42 = ChoiceNew(question=newQuestion4, choice_text="No", votes=0, is_selected=False)
            # newChoice43 = ChoiceNew(question=newQuestion4, choice_text="Not really sure", votes=0, is_selected=False)

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
            newChoice51 = ChoiceNew(question=newQuestion5, choice_text="Sales-oriented", votes=0, is_selected=False)
            newChoice52 = ChoiceNew(question=newQuestion5, choice_text="Media", votes=0, is_selected=False)
            newChoice53 = ChoiceNew(question=newQuestion5, choice_text="Interactives", votes=0, is_selected=False)
            newChoice54 = ChoiceNew(question=newQuestion5, choice_text=CHOICE_TEXT, votes=0, is_selected=False)

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

        # proceed to add choices to question 6 if not already done
        if len(newQuestion7.choicenew_set.all()) <= 0:
            newChoice71 = ChoiceNew(question=newQuestion7, choice_text="Sales-oriented", votes=0, is_selected=False)
            newChoice72 = ChoiceNew(question=newQuestion7, choice_text="Media", votes=0, is_selected=False)
            newChoice73 = ChoiceNew(question=newQuestion7, choice_text="Interactives", votes=0, is_selected=False)
            newChoice74 = ChoiceNew(question=newQuestion7, choice_text=CHOICE_TEXT, votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice71.save()
                    print("XXX: newChoice71.save() OK")
                    newChoice72.save()
                    print("XXX: newChoice72.save() OK")
                    newChoice73.save()
                    print("XXX: newChoice73.save() OK")
                    newChoice74.save()
                    print("XXX: newChoice74.save() OK")
            except IntegrityError:
                print("FAILED7: there has been an error")

        # proceed to add choices to question 4-1 which is basically the optional input box if not already done
        if len(newQuestion71.choicenew_set.all()) <= 0:
            newChoice71 = ChoiceNew(question=newQuestion71, choice_text="  ", votes=0, is_selected=False)

            try:
                with transaction.atomic():
                    newChoice71.save()
                    print("XXX: newChoice71.save() OK")
            except IntegrityError:
                print("FAILED71: there has been an error")

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
    print('showSurveyLinksWithPage: currentQuestionPage.questionnew_set.all()')
    for s in currentQuestionPage.questionnew_set.all():
        print(s)
    return render(request, 'survey/indexLinks.html', {'questionPage': currentQuestionPage, 'pageNumber':pageNumber, 'showAlert': showAlert})

# def surveyDetail(request, question_id):
#     # XXX
#     # question = get_object_or_404(Question, pk=question_id)
#     question = get_object_or_404(QuestionNew, pk=question_id)
#     return render(request, 'survey/detail.html', {'question': question})
#
# # def surveyDetailView(DetailView):
# #     model = Question
# #     template_name = 'survey/detail.html'
# # #
def surveyResults(request, question_id):
    # XXX
    # question = get_object_or_404(Question, pk=question_id)
    question = get_object_or_404(QuestionNew, pk=question_id)
    return render(request, 'survey/results.html', {'question': question})

# def surveyResultsView(DetailView):
#     model = Question
#     template_name = 'survey/results.html'


def surveyResultsNew(request, question_page_id):
    # XXX
    # question = get_object_or_404(Question, pk=question_id)
    questionPage = get_object_or_404(QuestionPage, pk=question_page_id)
    return render(request, 'survey/resultsLinks.html', {'question_page': questionPage})

# def surveyResultsView(DetailView):
#     model = Question
#     template_name = 'survey/results.html'

def surveyVote(request, question_id):
    print('entered: surveyVote')
    # XXX
    # question = get_object_or_404(Question, pk=question_id)
    question = get_object_or_404(QuestionNew, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # XXX
    # except (KeyError, Choice.DoesNotExist):
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


"""
For each question from the question page, get 
the choice selected by the user and log it 
"""
def extractAndMarkAnswersFromRequest(request, questionPage, q, validChoices, otherChoicesMap):
    selected_question = questionPage.questionnew_set.get(question_text=questions[q])
    selected_choice = selected_question.choicenew_set.get(pk=request.POST['choice_for_question_text_' + questions[q]])
    if CHOICE_TEXT in selected_choice.choice_text:
        # the user selected the other option for this question
        print("surveyVoteNew(): extractAndLogAnswers(): Found", CHOICE_TEXT, "selected for Question", str(q + 1), ": ", selected_question)
        otherChoicesMap[q] = True
    selected_choice.is_selected = True
    selected_choice.votes += 1
    print("surveyVoteNew(): extractAndLogAnswers(): Question", str(q + 1), ": ", selected_question)
    print("surveyVoteNew(): extractAndLogAnswers(): Choice", str(q + 1), ": ", selected_choice)
    validChoices.append(selected_choice)
    print("surveyVoteNew(): extractAndLogAnswers(): appended as valid choice!")

    if q == 0:
        #  if the user selected YES to the question "Did you click on this link ?"
        #  then mark the corresponding link model is_clicked field to True
        if selected_choice.choice_text.lower().strip() == "yes".strip():
            print("surveyVoteNew(): extractAndLogAnswers(): This is a YES")
            questionPage.link_model.is_clicked = True
            # save this change
            questionPage.link_model.save()

def surveyVoteNew(request, question_page_id, page_number):
    print('surveyVoteNew(): entered with question_page_id: ' + str(question_page_id) + ", pageNumber: " + str(page_number))
    print(request.POST)
    questionPage = get_object_or_404(QuestionPage, pk=question_page_id)
    currentUserId = questionPage.user.id
    print('surveyVoteNew(): extracted user id: ' + str(currentUserId))
    try:
        validChoices = []
        otherChoiceMap = defaultdict(bool)
        for q in questions:
            extractAndMarkAnswersFromRequest(request, questionPage, q, validChoices, otherChoiceMap)
        print("surveyVoteNew(): otherChoiceMap: " + str(otherChoiceMap))
        # extract the specified text from the input box of the following question of each question
        # where the user selected the @{CHOICE_TEXT}(Other(please specify...)) as the answer
        for questionWithOtherOptionSelected in otherChoiceMap:
            questionKeyWhichContainsTextForOtherOption = questionWithOtherOptionSelected * 10 + 1  # 2 -> 2*10 + 1 = 21, 3 -> 3*10 + 1 = 31, 6 = 6*10 + 1 = 61
            questionWithTextForOtherOption = questionPage.questionnew_set.get(question_text=questions[questionKeyWhichContainsTextForOtherOption])
            selectedChoiceForQuestionWithTextForOtherOption = questionWithTextForOtherOption.choicenew_set.all()[0]
            choiceText = request.POST['choice_for_question_text_' + questions[questionKeyWhichContainsTextForOtherOption]]
            if not choiceText.strip():
                raise KeyError('surveyVoteNew(): otherOption: no text specified for question: ' + str(questions[questionKeyWhichContainsTextForOtherOption]))
            # at this point if the above key is not found in the request then this means that the user did select the Other option
            # for the question but did not type in any text against it. This will throw a KeyError and we will not proceed with saving these choices
            print("surveyVoteNew(): otherOption: Question:", str(questionWithTextForOtherOption))
            print("surveyVoteNew(): otherOption: SelectedChoice:", str(selectedChoiceForQuestionWithTextForOtherOption))
            print("surveyVoteNew(): otherOption: ChoiceText:", choiceText)
            selectedChoiceForQuestionWithTextForOtherOption.choice_text = choiceText
            selectedChoiceForQuestionWithTextForOtherOption.is_selected = True
            selectedChoiceForQuestionWithTextForOtherOption.votes += 1
            validChoices.append(selectedChoiceForQuestionWithTextForOtherOption)

        # save all requests to db since none of them caused an error
        for q, selected_choice in enumerate(validChoices):
            selected_choice.save()
            print("surveyVoteNew(): success: saved choice: ", str(q + 1), ': ', str())

        # extract answer to question 1
        #
        # # extract answer to question 2
        # selected_question = questionPage.questionnew_set.get(question_text=questions[1])
        # print("surveyVoteNew(): Question2: ", selected_question)
        # selected_choice2 = selected_question.choicenew_set.get(pk=request.POST['choice_for_question_text_' + questions[1]])
        # print("surveyVoteNew(): Choice2: ", selected_choice2)
        #
        # # # extract answer to question 3 - this is an input box
        # # selected_question = questionPage.questionnew_set.get(question_text=questions[2])
        # # print("surveyVoteNew(): Question3: ", selected_question)
        # # selected_choice3 = selected_question.choicenew_set.all()[0]
        # # selected_choice3_text = request.POST['choice_for_question_text_' + questions[2]]
        # # print("surveyVoteNew(): Choice3: ", selected_choice3)
        # # print("surveyVoteNew(): Choice3Text: ", selected_choice3_text)
        #
        # # extract answer to question 3
        # selected_question = questionPage.questionnew_set.get(question_text=questions[2])
        # print("surveyVoteNew(): Question3: ", selected_question)
        # selected_choice3 = selected_question.choicenew_set.get(pk=request.POST['choice_for_question_text_' + questions[2]])
        # print("surveyVoteNew(): Choice3: ", selected_choice3)
        #
        #
        # # extract answer to question 4
        # selected_question = questionPage.questionnew_set.get(question_text=questions[3])
        # print("surveyVoteNew(): Question4: ", selected_question)
        # selected_choice4 = selected_question.choicenew_set.get(pk=request.POST['choice_for_question_text_' + questions[3]])
        # print("surveyVoteNew(): Choice4: ", selected_choice4)

    except (KeyError, ChoiceNew.DoesNotExist):
        # Redisplay the questionPage voting form.
        # return render(request, 'survey/detail.html', {
        print("surveyVoteNew(): failure: something went wrong in selecting choice")
        # return render(request, 'survey/index.html', {
        #     'question': questionPage,
        #     'error_message': "You didn't select a choice.",
        # })
        return HttpResponseRedirect(reverse('showSurveyLinksWithPage', args=(currentUserId, int(page_number), 1)))
    else:
        # XXX
        # # time to save this QuestionPage with all the answered questions
        # selected_choice1.is_selected = True
        # selected_choice1.votes += 1
        # selected_choice1.save()
        # print("surveyVoteNew(): success: saved choice 1")
        #
        # selected_choice2.is_selected = True
        # selected_choice2.votes += 1
        # selected_choice2.save()
        # print("surveyVoteNew(): success: saved choice 2")
        #
        # selected_choice3.choice_text = selected_choice3_text
        # selected_choice3.is_selected = True
        # selected_choice3.votes += 1
        # selected_choice3.save()
        # print("surveyVoteNew(): success: saved choice 3")
        #
        # selected_choice4.is_selected = True
        # selected_choice4.votes += 1
        # selected_choice4.save()

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
        return HttpResponseRedirect(reverse('showSurveyLinksWithPage', args=(currentUserId, int(page_number) + 1, 0)))

def surveyVoteNewBypass(request, question_page_id, page_number, bypass):
    print('surveyVoteNew(): entered with question_page_id: ' + str(question_page_id) + ", pageNumber: " + str(page_number))
    print(request.POST)
    questionPage = get_object_or_404(QuestionPage, pk=question_page_id)
    currentUserId = questionPage.user.id
    return HttpResponseRedirect(reverse('showSurveyLinksWithPage', args=(currentUserId, int(page_number) + 1, 0)))
