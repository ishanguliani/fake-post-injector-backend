"""djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from todo.views import todoView, addTodo, deleteTodo
# from twitter.views import twitterView
from django.conf.urls.static import static
from django.conf import settings
from welcome.views import signupSuccess, signupFailed, showWelcomePage
from form.views import showForm
from welcome.views import showWelcomePage
from user.views import createUser
from django.views.generic.base import RedirectView
# from survey.views import showSurveyView, surveyDetailView, surveyResultsView, surveyVote
from survey.views import showSurveyLinks, surveyResults,surveyResultsNew, surveyVote, surveyVoteNew, surveyVoteNewBypass
from survey.views import showSurveyLinksWithPage
from link.views import saveOriginalLink
from fakeLinkModel.views import getData
from configuration.views import getConfiguration

admin.site.site_header = "Center For Cybersecurity"
admin.site.site_title = "Center For Cybersecurity"
admin.site.index_title = "You are viewing live data..."

urlpatterns = [
    path('welcome/', showWelcomePage, name="showWelcomePage"),
    path('', showWelcomePage, name="showWelcomePage"),
    path('admin/', admin.site.urls),
    path('todo/', todoView),
    path('addTodo/', addTodo),
    path('deleteTodo/<int:todoId>/', deleteTodo),
    # path('twitter/', twitterView),
    # path('', twitterView, name='twitterView'),
    path('form/', showForm, name='showForm'),
    path('person/', include('person.urls')),
    path('addNewFacebookUser/', include('person.urls')),
    # path('survey/', showSurvey, name='showSurvey'),
    path('surveyLinks/<int:userId>/<int:pageNumber>/', showSurveyLinksWithPage, name='showSurveyLinksWithPage'),
    path('surveyLinks/<int:userId>/<int:pageNumber>/<int:showAlert>/', showSurveyLinksWithPage, name='showSurveyLinksWithPage'),
    path('surveyLinks/<int:id>/', showSurveyLinks, name='showSurveyLinks'),
    # path('surveyLinks/', showSurveyLinks, name='showSurveyLinks'),
    # path('survey/<int:question_id>/', surveyDetail, name='surveyDetail'),
    path('survey/<int:question_id>/results/', surveyResults, name='surveyResults'),
    path('survey/<int:question_page_id>/results/', surveyResultsNew, name='surveyResultsNew'),
    # path('survey/<int:question_id>/vote/', surveyVote, name='surveyVote'),
    path('survey/<int:question_page_id>/<int:page_number>/', surveyVoteNew, name='surveyVoteNew'),
    path('survey/<int:question_page_id>/<int:page_number>/<int:bypass>/', surveyVoteNewBypass, name='surveyVoteNewBypass'),
    # path('survey/', showSurveyView, name='showSurveyView'),
    # path('survey/<int:pk>/', surveyDetailView, name='surveyDetailView'),
    # path('survey/<int:pk>/results/', surveyResultsView, name='surveyResultsView'),
    # path('survey/<int:pk>/vote/', surveyVote, name='surveyVote'),
    path('signup/', createUser, name="createUser"),
    path('signupSuccess/<int:id>', signupSuccess, name="signupSuccess"),
    path('signupFailed/', signupFailed, name="signupFailed"),
    path('redirect/', showWelcomePage, name="showWelcomePage"),
    path('redirectToFacebook/',
         RedirectView.as_view(url='https://facebook.com/')),
    path('link/saveOriginal/', saveOriginalLink, name="saveOriginalLink"),
    # get fake links data
    path('getFakeLinks/', getData, name="getFakeLinks"),
    path('getConfiguration/', getConfiguration, name="getConfiguration"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
