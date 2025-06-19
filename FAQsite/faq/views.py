from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Question, Answer
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from django.db.models import Q, Prefetch

def faq_view(request):
    if request.user.is_staff:
        return redirect('/admin/')

    categories = {
        'service': 'Service Complaint',
        'policy': 'Policies',
        'account': 'Account & Billing',
        'app': 'Application Issues'
    }

    categorized_questions = {}

    for key, label in categories.items():
        # Build a query: public questions for everyone
        query = Q(category=key, visibility='public', is_answered=True)

        # If logged-in user: also allow their private questions
        if request.user.is_authenticated:
            query |= Q(category=key, visibility='private', user=request.user)

        questions = Question.objects.filter(query) \
            .prefetch_related(
                Prefetch('answers', queryset=Answer.objects.select_related('user'))
            ).order_by('-created_at')

        categorized_questions[label] = questions

    return render(request, 'faq.html', {
        'categorized_questions': categorized_questions
    })

from .forms import QuestionForm

@login_required
def ask_question(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        question = request.POST.get('question')
        category = request.POST.get('category')
        visibility = request.POST.get('visibility')
        if title and question and category:
            Question.objects.create(
                user=request.user,
                title=title,
                question=question,
                category=category,
                visibility=visibility

            )
            messages.success(request, "Your question has been submitted.")
            return redirect('faq_list')  # change this to your FAQ page name
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'ask_question.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')  # redirect to Django's login view
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})