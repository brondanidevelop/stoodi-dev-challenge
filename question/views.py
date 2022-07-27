#coding: utf8
from django.shortcuts import render
from .models import Question, Answer, History

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

def check_question(question_order, answer_selected):
    answer = Answer.objects.filter(
        question__order=question_order,
        order__exact=answer_selected,
        is_active=True,
        is_correct_answer=True).exists()

    return answer

def next_question(question_order):
    queryset = Question.objects.filter(
        is_active=True,
        order__gt=question_order
    )
    if queryset.exists():
        queryset = queryset.only('id', 'order').order_by('order')
        return queryset[0].order

    return 1

def register_history(user, question_ref, answer_selected, is_correct):
    history = History()
    history.question = Question.objects.get(id=question_ref)
    history.answer_selected = answer_selected
    history.is_correct = is_correct
    history.user = user if user.is_authenticated else None
    history.save()

def question_answer(request):
    question_order = request.POST.get('question_order', None)
    question_ref = request.POST.get('question_ref', None)
    answer_selected = request.POST.get('answer', 'z')

    is_correct = check_question(question_order, answer_selected)
    question = next_question(int(question_order)) if is_correct else question_order

    register_history(request.user,question_ref, answer_selected, is_correct)

    context = {
        'is_correct': is_correct,
        'next': question
    }

    return render(request, 'question/answer.html', context=context)