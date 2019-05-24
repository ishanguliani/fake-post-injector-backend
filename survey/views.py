# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from .models import Question, QuestionNew, ChoiceNew, QuestionPage
from user.models import User
from link.models import LinkModel
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

#
# def showSurveyView(ListView):
#     template_name = 'survey/index.html'
#     context_object_name = 'latest_question_list'
#     def get_queryset(self):
#         return Question.objects.all()

def showSurvey(request):
    # return render(request, "survey/surveyForm.html", {'form': SurveyModelForm()})
    # XXX
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    latest_question_list = QuestionNew.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'survey/index.html', context)

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
    latest_question_list = QuestionNew.objects.order_by('-pub_date')[:5]

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
    print("XXX: passing : ", str(allQuestionPages[0]))
    print("XXX: questions on this page : total : " + str(len(allQuestionPages[0].questionnew_set.all())))
    # for i, choice in enumerate(allQuestionPages[0].questionnew_set.objects.all()):
    #     print("XXX: choice", i, ": ", choice)

    return render(request, 'survey/indexLinks.html', {'questionPage': allQuestionPages[0]})

    # return render(request, 'survey/indexLinks.html', {'allLinks': allLinks, 'latest_question_list': latest_question_list})

def showSurveyLinksWithPage(request, id, pageNumber):

    # print('entered showSurveyLinks() with id:', str(id), "and pageNumber:", str(pageNumber))
    # if not id or not pageNumber:
    #     print('showSurveyLinks(): no id received')
    #     return
    # # get the current user
    # currentUser = User.objects.filter(pk=id)[0]
    # if not currentUser:
    #     print('showSurveyLinks(): user not found')
    #     return
    # print('showSurveyLinks(): success: user details: ', str(currentUser))
    # # get all the question pages associated with the current user
    # allQuestionPages = get_list_or_404(QuestionPage, user=currentUser)
    # if not allQuestionPages:
    #     print('showSurveyLinks(): allQuestionPages not found!')
    #     return
    # print('showSurveyLinks(): success: found ' + str(len(allQuestionPages)) + ' pages')
    # print("XXX: passing : ", str(allQuestionPages[pageNumber]))
    # print("XXX: questions on this page : total : " + str(len(allQuestionPages[0].questionnew_set.all())))
    # return render(request, 'survey/indexLinks.html', {'questionPage': allQuestionPages[0]})
    return None

def showNextQuestionPage():
    pass

def surveyDetail(request, question_id):
    # XXX
    # question = get_object_or_404(Question, pk=question_id)
    question = get_object_or_404(QuestionNew, pk=question_id)
    return render(request, 'survey/detail.html', {'question': question})

# def surveyDetailView(DetailView):
#     model = Question
#     template_name = 'survey/detail.html'
# #
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

def surveyVoteNew(request, question_page_id):
    print('entered: surveyVoteNew with request post')
    print(request.POST)
    questionPage = get_object_or_404(QuestionPage, pk=question_page_id)

    try:
        selected_question = questionPage.questionnew_set.get(pk=1)
        print("surveyVoteNew(): Question: ", selected_question)
        selected_choice = selected_question.choicenew_set.get(pk=request.POST['choice_for_question_id_1'])
        print("surveyVoteNew(): Choice: ", selected_choice)

        selected_question = questionPage.questionnew_set.get(pk=2)
        print("surveyVoteNew(): Question: ", selected_question)
        selected_choice = selected_question.choicenew_set.get(pk=request.POST['choice_for_question_id_2'])
        print("surveyVoteNew(): Choice: ", selected_choice)

        selected_question = questionPage.questionnew_set.get(pk=3)
        print("surveyVoteNew(): Question: ", selected_question)
        selected_choice = request.POST['choice_for_question_id_3']
        print("surveyVoteNew(): Choice: ", selected_choice)

        selected_question = questionPage.questionnew_set.get(pk=4)
        print("surveyVoteNew(): Question: ", selected_question)
        selected_choice = selected_question.choicenew_set.get(pk=request.POST['choice_for_question_id_4'])
        print("surveyVoteNew(): Choice: ", selected_choice)

    # XXX
    except (KeyError, ChoiceNew.DoesNotExist):
        # Redisplay the questionPage voting form.
        # return render(request, 'survey/detail.html', {
        return render(request, 'survey/index.html', {
            'question': questionPage,
            'error_message': "You didn't select a choice.",
        })
    else:


        # selected_choice.votes += 1
        # selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('surveyResultsNew', args=(questionPage.id,)))