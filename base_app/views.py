from django.shortcuts import render, redirect

# Create your views here.

from .models import Roger_preprep_line, Todo_obj, Todo_phase
from .forms import Form_Roger_preprep_line

def home(request):
    return render(request, 'base_app/home.html')

def roger_man(request):
    rogers_lines = Roger_preprep_line.objects.all()
    context = {'rogers_lines': rogers_lines}
    return render(request, 'base_app/roger_man.html', context)

def roger_response(request, pk):
    context = {'input_var': Roger_preprep_line.objects.get(name=pk).line} # All primary key referenes should be remade for actual IDs instead of strings
    return render(request, 'base_app/roger_response.html', context)

def roger_create_response(request):
    context = {'form': Form_Roger_preprep_line()}
    if request.method == 'POST':
        form = Form_Roger_preprep_line(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Roger Man')
    return render(request, 'base_app/roger_form.html', context)

def todo_list(request):
    context = {'objectives': Todo_obj.objects.all()}
    return render(request, 'base_app/todo_list.html', context)

def todo_obj(request, pk):
    context = {'objective': Todo_obj.objects.get(name=pk), 'phases': Todo_phase.objects.filter(objective__name=pk)}
    return render(request, 'base_app/todo_obj.html', context)