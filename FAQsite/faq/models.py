from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Create your models here.


class Question(models.Model):
    CATEGORY_CHOICES = [
        ('service', 'Service Complaint'),
        ('account', 'Account & Billing'),
        ('policy', 'Policies'),
        ('app', 'Application Issues'),
        ('other', 'Other'),
    ]

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='questions'
    )
    title = models.CharField(max_length=200)
    question = models.CharField(max_length=355)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='other')
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({'Answered' if self.is_answered else 'Unanswered'})"


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers'
    )
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='answers'
    )
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=Answer)
def mark_question_as_answered(sender, instance, created, **kwargs):
    if created and not instance.question.is_answered:
        instance.question.is_answered = True
        instance.question.save()

@receiver(post_delete, sender=Answer)
def unmark_question_if_no_answers(sender, instance, **kwargs):
    question = instance.question
    if not question.answers.exists():
        question.is_answered = False
        question.save()
    

   
