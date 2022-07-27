# coding: utf8
from django.test import TestCase, RequestFactory
from question.models import Question, Answer

class questionModelTestCase(TestCase):

    def setUp(self):
        self.Question = Question.objects.create(
            question_text = 'nova pergunta?',
            order = 1
        )

    def test_new_question(self):
        """Teste que verifica se a questão está cadastrado com suas respectivas características"""
        self.assertEqual(self.question.question_text, 'nova pergunta?')
        self.assertEqual(self.question.order, 1)

class AnswerModelTestCase(TestCase):
    def setUp(self):
        new_question = self.Question = Question.objects.create(
            question_text = 'nova pergunta?',
            order = 1
        )
        self.answer = Answer.objects.create(
            question = new_question,
            answer_text = 'uma resposta',
            order = 'a',
            is_correct_answer = True
        )

    def test_new_answer(self):
        """Teste que verifica se a resposta está cadastrado com suas respectivas características"""
        self.assertEqual(self.answer.question.question_text, 'nova pergunta?')
        self.assertEqual(self.answer.answer_text, 'uma resposta')
        self.assertEqual(self.answer.order, 'a')
        self.assertEqual(self.answer.is_correct_answer, True)