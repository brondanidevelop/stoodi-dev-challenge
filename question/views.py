#coding: utf8
from django.shortcuts import render
from .models import Question, Answer

def get_answer(question_pk):
    queryset = Answer.objects.filter(
        is_active=True, question=question_pk
    ).only('id', 'answer_text', 'order').order_by('order')

    return queryset

def get_question(next=1):
    queryset = Question.objects.filter(
        is_active=True,
        order=next
    ).only('id', 'question_text', 'order').order_by('order')

    return queryset[0]

def question(request):
    next = int(request.GET.get('next', 1))
    question = get_question(next)
    answer = get_answer(question.id)

    if not answer.count():
        question = get_question(1)
        answer = get_answer(question.id)

    context = {
        'question': question,
        'answers': answer,
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
