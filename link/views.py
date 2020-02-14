from django.shortcuts import render
from django.http import JsonResponse
from link.QUESTIONS import questions
from .models import LinkModel, LinkType
from user.models import User
import datetime
from django.views.decorators.csrf import csrf_exempt
from linkPreview.models import LinkPreviewModel, ParentLink
from survey.models import QuestionPage, QuestionNew, QuestionType, ChoiceNew
import requests, json
from django.db import transaction, IntegrityError

# Create your views here.

PREVIEW_BASE_URL = "http://api.linkpreview.net/?key=5cd32a757565b4e17f2a258effb8ae350f8a8062d9a4c&q="

@csrf_exempt
def saveOriginalLink(request):
    if request.method == 'POST':
        user_id = request.META.get('HTTP_USERID', 'XXX')
        # return False if no header found
        if user_id == 'XXX':
            return JsonResponse({'success': False, 'message': 'Did you forget to include a valid user_id in the header?'})
        print('Received request from user_id:', user_id)
        link_text_original = request.POST.get('link_text_original', 'XXX')
        link_text_fake = request.POST.get('link_text_fake', 'XXX')
        link_target_original = request.POST.get('link_target_original', 'XXX')
        link_target_fake= request.POST.get('link_target_fake', 'XXX')
        authored_text_original = request.POST.get('authored_text_original', 'XXX')
        authored_text_fake = request.POST.get('authored_text_fake', 'XXX')
        link_image_src_original = request.POST.get('link_image_src_original', 'XXX')
        link_type = request.POST.get('link_type', 'XXX')
        author_name = request.POST.get('author_name', 'XXX')
        is_clicked = request.POST.get('is_clicked', 'False')
        is_seen = bool(request.POST.get('is_seen', 'XXX'))
        print('received: ',
              'link_text_original:', str(link_text_original), ", ",
              'link_text_fake:', str(link_text_fake), ", ",
              "link_target_original:", str(link_target_original), ", ",
              "link_target_fake:", str(link_target_fake), ", ", end=", ")
        print('authored_text_original:', str(authored_text_original),
              ", link_image_src_original:", str(link_image_src_original),
              ", link_type:", str(link_type), end=", ")
        print('authored_text_fake:', str(authored_text_fake), end=", ")
        print('author_name:', str(author_name), end=", ")
        print('is_clicked:', is_clicked, ", is_seen:", is_seen)
        import re
        if re.match("^[fF]", is_clicked):
            print("is_clicked is false" )
            is_clicked = False
        else:
            print("is_clicked is true")
            is_clicked = True

        # now check if the preview data for this particular link_target_fake is available in the database
        parentLink = ParentLink.objects.filter(parent_link=link_target_fake)
        newLinkPreviewModel = None
        if not parentLink:
            print("saveOriginalLink(): parentLink: not found for", link_target_fake)
            # this means that there no valid mapping for this parent link
            # hence an API call needs to be made to get and store its preview data
            # create new parent link
            newParentLink = ParentLink(parent_link = link_target_fake)
            # add this parent link to database
            newParentLink.save()
            print("saveOriginalLink(): newParentLink saved: success: ", newParentLink)

            # get the API data for this parent link
            requestUrl = PREVIEW_BASE_URL + link_target_fake
            print("saveOriginalLink(): requestUrl: ", requestUrl)
            r = requests.get(requestUrl)
            responseMap = json.loads(r.text)
            # create a new link preview model
            newLinkPreviewModel = LinkPreviewModel(parent_link = newParentLink, title = responseMap['title'], description = responseMap['description'], image = responseMap['image'], url = responseMap['url'])
            newLinkPreviewModel.save()
            print("saveOriginalLink(): newLinkPreviewModel saved: success: ", newLinkPreviewModel)
        else:
            print("saveOriginalLink(): parentLink: found for", link_target_fake)
            # get the link preview model associated with this parent link
            newLinkPreviewModel = LinkPreviewModel.objects.filter(parent_link = parentLink[0])
            if not newLinkPreviewModel:
                print("saveOriginalLink(): newLinkPreviewModel: not found for", parentLink)
                return JsonResponse({'success': False, 'message': 'could not restore saved newLinkPreviewModel'})
            newLinkPreviewModel = newLinkPreviewModel[0]

        print('preview_title:', newLinkPreviewModel.title, ", preview_description:", newLinkPreviewModel.description)
        print('preview_image:', newLinkPreviewModel.image, ", preview_url:", newLinkPreviewModel.url)

        mUser = User.objects.filter(uuid=user_id)[0]

        origLinkModel = LinkModel(link_text_original = link_text_original, link_text_fake = link_text_fake,
                                  link_target_original = link_target_original, link_target_fake = link_target_fake, link_image_src_original = link_image_src_original,
                                  link_type = LinkType.objects.filter(pk=int(link_type))[0], authored_text_original = authored_text_original,
                                  authored_text_fake = authored_text_fake, author_name = author_name,
                                  is_seen = is_seen, is_clicked = is_clicked, time_to_view = datetime.datetime.now().time(),
                                  user = mUser,
                                  preview_title  = newLinkPreviewModel.title,
                                  preview_description = newLinkPreviewModel.description,
                                  preview_image = newLinkPreviewModel.image,
                                  preview_url = newLinkPreviewModel.url)
        # save the model
        origLinkModel.save()

        print("XXX: creating new page")
        # also save a new question page
        # create a new question page and add to question page list
        newQuestionPage = QuestionPage(user=mUser, link_model=origLinkModel)
        # save this question page
        newQuestionPage.save()
        print("XXX: created and saved new page: " + str(newQuestionPage))
        # next task it to link questions with this newQuestionPage
        # since Question model has a many to many relationship with QuestionPage,
        # we can just add this page as a ManyToMany field to all the questions

        # XXX
        # create and add new questions

        # create and add new questions to this page
        # newQuestion1 = QuestionNew(question_text=questions[0],
        #                           question_type=QuestionType.objects.get(question_type=1),
        #                           question_page=newQuestionPage)
        #
        # # newQuestion1.save()
        # newQuestion2 = QuestionNew(question_text=questions[1],
        #                            question_type=QuestionType.objects.get(question_type=1),
        #                            question_page=newQuestionPage)
        # # newQuestion2.save()
        # newQuestion3 = QuestionNew(question_text=questions[2],
        #                            question_type=QuestionType.objects.get(question_type=2),
        #                            question_page=newQuestionPage)
        # # newQuestion3.save()
        # newQuestion4 = QuestionNew(question_text=questions[3],
        #                            question_type=QuestionType.objects.get(question_type=1),
        #                            question_page=newQuestionPage)
        # newQuestion4.save()
        # QuestionNew.objects.bulk_create([newQuestion1, newQuestion2, newQuestion3, newQuestion4])


        # newQuestion1.save()
        # newQuestion2.save()
        # newQuestion3.save()
        # newQuestion4.save()

        # try:
        #     with transaction.atomic():
        #         newQuestion1.save()
        #         newQuestion2.save()
        #         newQuestion3.save()
        #         newQuestion4.save()
        # except IntegrityError:
        #     print("FAILED1: there has been an error")

        # print("XXX: saved questions[0]")
        # newChoice11 = ChoiceNew(question=newQuestion1, choice_text="Entertainment")
        # print("newChoice11 id: " + newChoice11.question.question_text)
        # newChoice12 = ChoiceNew(question=newQuestion1, choice_text="News")
        # newChoice13 = ChoiceNew(question=newQuestion1, choice_text="Sports")
        # newChoice14 = ChoiceNew(question=newQuestion1, choice_text="Interactive")
        # newChoice15 = ChoiceNew(question=newQuestion1, choice_text="Public page")
        # # newChoice11.save()
        # # newChoice12.save()
        # # newChoice13.save()
        # # newChoice14.save()
        # # newChoice15.save()
        # print("XXX: saved 5 choices")
        #
        #
        # print("XXX: saved questions[1]")
        # newChoice21 = ChoiceNew(question=newQuestion2, choice_text="Spouse, Boyfriend/Girlfriend")
        # newChoice22 = ChoiceNew(question=newQuestion2, choice_text="Parents")
        # newChoice23 = ChoiceNew(question=newQuestion2, choice_text="Acquaintance")
        # newChoice24 = ChoiceNew(question=newQuestion2, choice_text="Close friends")
        # # newChoice21.save()
        # # newChoice22.save()
        # # newChoice23.save()
        # # newChoice24.save()
        # print("XXX: saved 4 choices")
        #
        #
        # print("XXX: saved questions[2]")
        # newChoice31 = ChoiceNew(question=newQuestion3, choice_text="type reason here")
        # # newChoice31.save()
        # print("XXX: saved 1 choice")
        #
        # print("XXX: saved questions[3]")
        # newChoice41 = ChoiceNew(question=newQuestion4, choice_text="Yes")
        # newChoice42 = ChoiceNew(question=newQuestion4, choice_text="No")
        # newChoice43 = ChoiceNew(question=newQuestion4, choice_text="Not sure")
        # # newChoice41.save()
        # # newChoice42.save()
        # # newChoice43.save()
        # print("XXX: saved 3 choices")
        #
        #
        # # try:
        # #     with transaction.atomic():
        # # newChoice11.save()
        #         # newChoice12.save()
        #         # newChoice13.save()
        #         # newChoice14.save()
        #         # newChoice15.save()
        #         # newChoice21.save()
        #         # newChoice22.save()
        #         # newChoice23.save()
        #         # newChoice24.save()
        #         # newChoice31.save()
        #         # newChoice41.save()
        #         # newChoice42.save()
        #         # newChoice43.save()
        # # except IntegrityError:
        # #     print("FAILED2: there has been an error")
        #
        # # ChoiceNew.objects.bulk_create([newChoice11, newChoice12, newChoice13, newChoice14, newChoice15, newChoice21, newChoice22, newChoice23, newChoice24, newChoice31, newChoice41, newChoice42, newChoice43])
        # # print("XXX: created and saved new page: " + str(newQuestionPage))
        # # for question in QuestionNew.objects.all():
        # #     print("XXX: adding new page to question: " + str(question))
        # #     # XXX
        # #     # question.question_page.add(newQuestionPage)
        # #     question.question_page.add(newQuestionPage)

        # print("XXX: added questionPage, questions and choices successfully!")
        print("XXX: added new empty questionPage successfully!")
        # print("XXX: created new page and linked question: " + str(newQuestionPage))

        return JsonResponse({'success': True, 'message': 'Link saved successfully'})

    # otherwise return False
    return JsonResponse({'success': False, 'message': 'Invalid request'})