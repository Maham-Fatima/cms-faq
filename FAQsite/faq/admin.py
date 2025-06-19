from django.contrib import admin
from .models import Question, Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'is_answered', 'created_at')
    list_filter = ('is_answered', 'category')
    search_fields = ('title', 'question', 'user__username')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'created_at')
    search_fields = ('answer', 'question__title', 'user__username')
