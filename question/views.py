#coding: utf8
from django.shortcuts import render
from .models import Question, Answer, History
from django.contrib.auth.decorators import login_required


def get_answer(question_pk):
    """ Retorna todas as respostas de uma questão"""
    queryset = Answer.objects.filter(
        is_active=True, question=question_pk
    ).only('id', 'answer_text', 'order').order_by('order')

    return queryset

def get_question(next=1):
    """ Retorna uma questão especifica pela order definida"""
    queryset = Question.objects.filter(
        is_active=True,
        order=next
    ).only('id', 'question_text', 'order').order_by('order')

    return queryset[0]

def question(request):
    """ Retorna para o html a questão"""
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


def check_question(question_order, answer_selected):
    """ Valida se existe uma resposta de acordo com a questão e a opção selecionada"""
    answer = Answer.objects.filter(
        question__order=question_order,
        order__exact=answer_selected,
        is_active=True,
        is_correct_answer=True).exists()

    return answer

def next_question(question_order):
    """Retorna a próxima questão"""
    queryset = Question.objects.filter(
        is_active=True,
        order__gt=question_order
    )
    if queryset.exists():
        queryset = queryset.only('id', 'order').order_by('order')
        return queryset[0].order

    return 1

def register_history(user, question_ref, answer_selected, is_correct):
    """Registra quem respondeu a questão, bem como o usuário a se está correta"""
    history = History()
    history.question = Question.objects.get(id=question_ref)
    history.answer_selected = answer_selected
    history.is_correct = is_correct
    history.user = user if user.is_authenticated else None
    history.save()

def question_answer(request):
    """ Corrige a questão"""
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

@login_required
def log_questoes(request):
    """ Retorna o histórico de respostas do usuário logado"""
    history = History.objects.filter(user=request.user).order_by('-answered_at')

    context = {
        'history': history,
    }

    return render(request, 'question/history.html', context=context)
