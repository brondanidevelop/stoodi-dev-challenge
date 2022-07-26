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
    question = request.POST.get('question', None)
    answer = request.POST.get('answer', 'z')

    is_correct = Answer.objects.filter(
        question=question, order__exact=answer, is_active=True, is_correct_answer=True).exists()

    context = {
        'is_correct': is_correct,
    }

    return render(request, 'question/answer.html', context=context)
