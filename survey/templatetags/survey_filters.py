from django import template

register = template.Library()

@register.filter(name='get_at_index')
def get_at_index(qSet, index):
    print("get_at_index(): entered with index: " + str(index))
    questions = []
    for q in qSet.values():
        questions.append(q)
    print("get_at_index: returning question: ", questions[index]['question_text'])
    return questions[index]['question_text']