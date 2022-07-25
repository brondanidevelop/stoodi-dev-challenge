from django.contrib import admin
from .models import Question
# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text','order', 'is_active', 'create_at','update_at','user_create','user_update')

    def save_model(self, request, obj, form, change):
        print(obj)
        if change:
            obj.user_update = request.user
        else:
            obj.user_create = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Question, QuestionAdmin)
