#coding: utf8
from django.shortcuts import render
from .models import Question, Answer

def question(request):
    question = Question.objects.filter(is_active=True)[0]
    text = question.question_text

    answers = Answer.objects.filter(question=question, is_active=True).only('answer_text', 'order').order_by('order')

    context = {
        'question_text': text,
        'answers': answers,
    }

    return render(request, 'question/question.html', context=context)

def question_answer(request):
    answer = request.POST.get('answer', 'z')
    is_correct = answer == 'd'

    context = {
        'is_correct': is_correct,
    }

    return render(request, 'question/answer.html', context=context)