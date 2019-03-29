# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Question, Choice
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
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'survey/index.html', context)


def surveyDetail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'survey/detail.html', {'question': question})
#
# def surveyDetailView(DetailView):
#     model = Question
#     template_name = 'survey/detail.html'
# #
def surveyResults(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'survey/results.html', {'question': question})

# def surveyResultsView(DetailView):
#     model = Question
#     template_name = 'survey/results.html'

def surveyVote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
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