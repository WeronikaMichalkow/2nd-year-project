from django.urls import path
from .views import askQ, listQ, answerQ


app_name = 'questions'  # 👈 Add this line to define the namespace

urlpatterns = [
    path('ask/', askQ, name='ask_q'),
    path('', listQ, name='list'),  # Now 'questions:list' will work
    path('answer/<int:question_id>/', answerQ, name='answer_q'),
]
