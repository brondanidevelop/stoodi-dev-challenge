from django.contrib import admin
from .models import Question, Answer
# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text','order', 'is_active', 'create_at','update_at','user_create','user_update')
    ordering = ['order']
    list_filter = ['is_active']

    def save_model(self, request, obj, form, change):
        if change:
            obj.user_update = request.user
        else:
            obj.user_create = request.user
        super().save_model(request, obj, form, change)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question','answer_text','order','is_correct_answer','create_at','update_at','is_active','user_create','user_update')
    ordering = ['question__order', 'order']
    list_filter = ['question__order','is_active', 'is_correct_answer']

    def save_model(self, request, obj, form, change):
        if change:
            obj.user_update = request.user
        else:
            obj.user_create = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
