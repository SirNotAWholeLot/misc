from django.shortcuts import render, redirect

# Create your views here.

from .models import Roger_preprep_line, Todo_obj, Todo_phase, Post_op, Post_reply
from .forms import Form_Roger_preprep_line, Form_Post_op, Form_Post_reply

def home(request):
    return render(request, 'base_app/home.html')

def roger_man(request): # Roger Man gets his database as the context for his 'menu' -> it can be just the names
    rogers_lines = Roger_preprep_line.objects.all()
    context = {'rogers_lines': rogers_lines}
    return render(request, 'base_app/roger_man.html', context)

def roger_response(request, pk): # For the response page, it's a specific entry from the db
    context = {'input_var': Roger_preprep_line.objects.get(id=pk).line} # All primary key referenes should be remade for actual IDs instead of strings
    return render(request, 'base_app/roger_response.html', context)

def roger_create_response(request):
    context = {'form': Form_Roger_preprep_line()} # Form is a basic django built-in form
    if request.method == 'POST':
        form = Form_Roger_preprep_line(request.POST)
        if form.is_valid(): # Filled out properly? Save and return to the menu
            form.save()
            return redirect('Roger Man')
    return render(request, 'base_app/roger_form.html', context)

def todo_list(request):
    context = {'objectives': Todo_obj.objects.all()}
    return render(request, 'base_app/todo_list.html', context)

def todo_obj(request, pk): # Specific objective page fetches the phases for that objective
    context = {'objective': Todo_obj.objects.get(id=pk), 'phases': Todo_phase.objects.filter(objective__id=pk)}
    return render(request, 'base_app/todo_obj.html', context)

def posts_list(request):
    context = {'posts': Post_op.objects.all()}
    return render(request, 'base_app/posts_list.html', context)

def posts_post(request, pk):
    context = {'original': Post_op.objects.get(id=pk), 'replies': Post_reply.objects.filter(op__id=pk)}
    return render(request, 'base_app/todo_obj.html', context)

def post_create_op(request):
    context = {'form': Form_Post_op()}
    if request.method == 'POST':
        form = Form_Post_op(request.POST)
        if form.is_valid():
            form.save()
            return redirect('User posts') # Should redirect to the newly created post page
    return render(request, 'base_app/posts_op_form.html', context)

def post_create_reply(request, pk):
    context = {'form': Form_Post_reply()}
    if request.method == 'POST':
        form = Form_Post_reply(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('posts_post', pk=pk) # Should return to the post page
            return redirect('posts/<str:pk>')
    return render(request, 'base_app/posts_reply_form.html', context)
