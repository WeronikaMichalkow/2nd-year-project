from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Question
from .forms import form_for_question, form_for_answer

def askQ(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.customer = request.user.customer  # Assuming every user has a related customer
            question.save()
            return redirect('list')  # Redirect to the question list or another page
    else:
        form = orm_for_question()
    return render(request, 'ask_q.html', {'form': form})

def listQ(request):
    questions = Question.objects.all()
    return render(request, 'list.html', {'questions': questions})

def answerQ(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        form = form_for_answer(request.POST, instance=question)
        if form.is_valid():
            question.answered = now()
            form.save()
            return redirect('list')
    else:
        form = form_for_answer(instance=question)
    return render(request, 'answer_q.html', {'form': form, 'question': question})
