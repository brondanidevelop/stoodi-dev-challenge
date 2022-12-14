from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Log_Question(models.Model):
    id = models.AutoField(primary_key=True)
    create_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    is_active = models.BooleanField(default=True)
    user_create =  models.ForeignKey(User, related_name='user_create', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    user_update =  models.ForeignKey(User, related_name='user_update', on_delete=models.CASCADE, editable=False, null=True, blank=True)

    def __str__(self):
        return str(self.id)

def validate_order(value):
    if value <= 0:
        raise ValidationError(
            '%(value)s is not an valid number',
            params={'value': value},
        )

class Question(Log_Question):
    question_text = models.CharField(max_length=200, unique=True, null=False, blank=False)
    order = models.PositiveIntegerField(default=1, unique=True, validators=[validate_order])
    
    def __str__(self):
        return self.question_text


LETTERS_CHOICES = [
    ('a', 'a'),
    ('b', 'b'),
    ('c', 'c'),
    ('d', 'd'),
    ('e', 'e'),
    ('f', 'f'),
    ('g', 'g'),
    ('h', 'h'),
    ('i', 'i'),
    ('j', 'j'),
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

    def save(self, *args, **kwargs):
        answers = Answer.objects.filter(is_correct_answer=True, question=self.question.id)

        if answers.exists():
            self.is_correct_answer = False

        super(Answer, self).save(*args, **kwargs)
        
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'answer_text'], name='unique_answer_iqual'),
            models.UniqueConstraint(fields=['question', 'order'], name='unique_answer_order')
        ]

class History(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_selected = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    user =  models.ForeignKey(User, related_name='History_user_create', on_delete=models.CASCADE, editable=False, default=None, null=True, blank=True)

