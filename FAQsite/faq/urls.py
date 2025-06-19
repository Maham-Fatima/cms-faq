from django.urls import path
from .views import faq_view, ask_question, register

urlpatterns = [
    path('', faq_view, name='faq_list'),
    path('ask/', ask_question, name='ask_question'),
    path('register/', register, name='register'),  
   
]
