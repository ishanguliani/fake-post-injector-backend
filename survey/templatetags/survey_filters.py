from django import template

register = template.Library()

@register.filter(name='get_at_index')
def get_at_index(qSet, index):
    questions = []
    for q in qSet.values():
        questions.append(q)
    print("get_at_index: type: questions[0]", type(questions[0]))
    return questions[index]['question_text']