from django.db import models
from django.contrib.auth.models import User


class Log_Question(models.Model):
    id = models.AutoField(primary_key=True)
    create_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    is_active = models.BooleanField(default=True)
    user_create =  models.ForeignKey(User, related_name='user_create', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    user_update =  models.ForeignKey(User, related_name='user_update', on_delete=models.CASCADE, editable=False, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Question(Log_Question):
    question_text = models.CharField(max_length=200, unique=True, null=False, blank=False)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.question_text


LETTERS_CHOICES = [
    ('0', 'a'),
    ('1', 'b'),
    ('2', 'c'),
    ('3', 'd'),
    ('4', 'e'),
    ('5', 'f'),
    ('6', 'g'),
    ('7', 'h'),
    ('8', 'i'),
    ('9', 'j'),
]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    order = models.CharField(max_length=1, choices=LETTERS_CHOICES, default='a')
    is_correct_answer = models.BooleanField(default=False)
    create_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    is_active = models.BooleanField(default=True)
    user_create =  models.ForeignKey(User, related_name='Answer_user_create', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    user_update =  models.ForeignKey(User, related_name='Answer_user_update', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    
    def __str__(self):
        return self.answer_text

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'is_correct_answer'], name='unique_correct_answer'),
            models.UniqueConstraint(fields=['question', 'answer_text'], name='unique_answer_iqual')
        ]