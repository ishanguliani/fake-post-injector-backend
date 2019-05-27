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

    class Meta:
        verbose_name = "Question Type"
        verbose_name_plural = "Question Types"

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
    is_answered = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name = "Question Page"
        verbose_name_plural = "Question Pages"

    def __str__(self):
        # return "QuestionPage{ " + str(self.id) + ", " + str(self.user) + ", " + str(self.link_model) + ", questionSet{ " + str(self.questionnew_set.all()) + "}, is_answered: " + str(self.is_answered)+ " }"
        return "QuestionPage{ " + str(self.id) + ", " + str(self.user) + ", " + str(self.link_model) + ", questionSet{ " + "}, is_answered: " + str(self.is_answered)+ " }"


class QuestionNew(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, null=False)
    question_page = models.ForeignKey(QuestionPage, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        selectedChoice = None
        for choice in self.choicenew_set.all():
            if choice.is_selected:
                selectedChoice = choice
                print("QuestionNew: choicenew_set: selected choice: " + str(selectedChoice))

        selectedChoiceString = "" if selectedChoice is None else str(selectedChoice)
        # selectedChoiceString = ""

        return "QuestionNew{ " + str(self.id) + ", " + str(self.question_text) + ", " \
               + "question_page{ " + str(self.question_page) + " }, " + str(
            self.question_type) + ", selected_choice: " + selectedChoiceString + ", " + " } }"
            #    + "question_page_foreign{ " + str(self.new_question_page) + " }, " + str(
            # self.question_type) + ", selected_choice: " + selectedChoiceString + ", " + " } }"
        # XXX

# class QuestionNew(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published', auto_now_add=True)
#     question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, null=False)
#     question_page = models.ForeignKey(QuestionPage, on_delete=models.CASCADE, null=True)
#
#     class Meta:
#         verbose_name = "QuestionNewNew"
#         verbose_name_plural = "QuestionsNewNew"
#
#     def __str__(self):
#         selectedChoice = None
#         for choice in self.choicenew_set.all():
#             if choice.is_selected:
#                 selectedChoice = choice
#                 print("QuestionNewNew: choicenew_set: selected choice: " + str(selectedChoice))
#
#         selectedChoiceString = "" if selectedChoice is None else str(selectedChoice)
#         return "QuestionNewNew{ " + str(self.id) + ", " + str(self.question_text) + ", " \
#                + "question_page{ " + str(self.question_page) + " }, " + str(
#             self.question_type) + ", selected_choice: " + selectedChoiceString + ", " + " } }"
#             #    + "question_page_foreign{ " + str(self.new_question_page) + " }, " + str(
#             # self.question_type) + ", selected_choice: " + selectedChoiceString + ", " + " } }"
#         # XXX

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
    is_selected = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        return "ChoiceNew{ " + str(self.id)+ ", text: " + self.choice_text + ", is_selected: " + str(self.is_selected)
