from django.db import models
from user.models import User
from link.models import LinkModel

# Create your models here.
from django.db import models
import datetime
from django.utils import timezone

class QuestionType(models.Model):
    """
    type: 1:    radio button
    type: 2:    input text
    """
    question_type = models.IntegerField(default=1, blank=False)
    question_tag = models.TextField(default='radio button', blank=False, max_length=100)

    def __str__(self):
        return "QuestionType{ " + str(self.id) + ", "  + str(self.question_type)+ ", " + str(self.question_tag) + " }"

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, null=False)
    link_model = models.ForeignKey(LinkModel, on_delete=models.CASCADE)

    def __str__(self):
        return "Question{ " + str(self.id) + ", " + str(self.question_text) + ", " + str(self.pub_date) + ", " + "user{ " + str(self.user) + " }, " + str(self.question_type) + ", link_model{ " + str(self.link_model) + " } }"

class QuestionPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link_model = models.ForeignKey(LinkModel, on_delete=models.CASCADE)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    # def __init__(self, user, link_model, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.user = user
    #     self.link_model = link_model

    def __str__(self):
        return "QuestionPage{ " + str(self.id) + ", " + str(self.user) + ", " + str(self.link_model) + ", questionSet{ " + str(self.questionnew_set.all()) + " }"


class QuestionNew(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, null=False)
    question_page = models.ManyToManyField(QuestionPage)

    def __str__(self):
        return "QuestionNew{ " + str(self.id) + ", " + str(self.question_text) + ", " \
               + "question_page{ " + str(self.question_page) + " }, " + str(self.question_type) + ", " + " } }"
        # return "QuestionNew{ " + str(self.id) + ", " + str(self.question_text) + ", " + str(self.pub_date) + ", " + str(self.question_type) + ", " + " }"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class ChoiceNew(models.Model):
    question = models.ForeignKey(QuestionNew, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return "ChoiceNew{ " + str(self.id)+ ", text: " + self.choice_text
