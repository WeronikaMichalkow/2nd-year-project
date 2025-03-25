from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Question
from .forms import form_for_question, form_for_answer
from store.models import Customer  

def askQ(request):
    if request.method == "POST":
        form = form_for_question(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # Assuming the user is logged in
            question.save()
            return redirect('questions:list')  # Correct way to redirect with app_name namespace
    else:
        form = form_for_question()

    return render(request, 'ask_q.html', {'form': form})


def listQ(request):
    questions = Question.objects.all()
    return render(request, 'list.html', {'questions': questions})  # ✅ Rendering list.html



def answerQ(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    # Check if the user is an admin (staff user)
    if not request.user.is_staff:
        return redirect('questions:list')  # Redirect non-admin users to the list of questions
    
    if request.method == "POST":
        form = form_for_answer(request.POST, instance=question)
        if form.is_valid():
            question.answered = now()  # Set the answer time
            form.save()
            return redirect('questions:answer_q')
    else:
        form = form_for_answer(instance=question)

    return render(request, 'answer_q.html', {'form': form, 'question': question})
