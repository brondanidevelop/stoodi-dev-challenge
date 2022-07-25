#coding: utf8
from django.shortcuts import render
from .models import Question

def question(request):
    question = Question.objects.filter(is_active=True)[0]
    text = question.question_text

    # BUG: as respostas estão ficando fora de ordem
    answers = {
        'a': '0',
        'b': '2',
        'c': '16',
        'd': '32',
        'e': '128',
    }

    sorted_answers = dict(sorted(answers.items(), key=lambda item: item[0]))

    context = {
        'question_text': text,
        'answers': sorted_answers,
    }

    return render(request, 'question/question.html', context=context)

def question_answer(request):
    answer = request.POST.get('answer', 'z')
    is_correct = answer == 'd'

    context = {
        'is_correct': is_correct,
    }

    return render(request, 'question/answer.html', context=context)