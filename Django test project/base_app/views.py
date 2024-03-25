from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Roger_preprep_line, Todo_obj, Todo_phase, Post_op, Post_reply
from .forms import Form_Roger_preprep_line, Form_Post_op, Form_Post_reply

# Create your views here.

def login_page(request): # 'login' is already a function
    variant = 'login'
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User not found") # Messages currently don't work for some reason
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # This method itself does not require authentification
            return redirect('/')
        else:
            messages.error(request, "Username or password is incorrect")
    context = {'variant': variant}
    return render(request, 'base_app/login_register.html', context)

def logout_page(request):
    logout(request)
    return redirect('/')

def register_page(request):
    variant = 'register'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Can do stuff with the user credentials here if required
            user.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Error registering user")
    context = {'variant': variant, 'form': UserCreationForm()}
    return render(request, 'base_app/login_register.html', context)

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
    # Replies can also be queried with Post_op.post_reply_set.all()
    context = {'original': Post_op.objects.get(id=pk), 'replies': Post_reply.objects.filter(original__id=pk)}
    return render(request, 'base_app/posts_post.html', context)

@login_required(login_url='Login') # Decorators are a new thing for me
def post_create_op(request):
    context = {'form': Form_Post_op()}
    if request.method == 'POST':
        form = Form_Post_op(request.POST)
        if form.is_valid():
            filled = form.save(commit=False)
            filled.poster = request.user
            filled.participants.add(request.user) # Automatically adding OP as a 'participant'
            filled.save()
            return redirect('/posts/item_id=' + str(filled.id)) # Should redirect to the newly created post page
    return render(request, 'base_app/posts_op_form.html', context)

@login_required(login_url='Login')
def post_edit_op(request, pk):
    post = Post_op.objects.get(id=pk)
    context = {'post': post, 'form': Form_Post_op(instance=post)}
    if request.user != post.poster: # Admins should be able to bypass this
        messages.error(request, "You do not have the rights for this")
        return redirect('/posts/item_id=' + str(pk))
    if request.method == 'POST':
        form = Form_Post_op(request.POST, instance=post)
        if form.is_valid():
            #filled = form.save(commit=False) # Should not be required for editing
            #filled.poster = request.user
            #filled.save()
            form.save()
            return redirect('User posts')
    return render(request, 'base_app/posts_op_form.html', context)

@login_required(login_url='Login')
def post_delete_op(request, pk):
    post = Post_op.objects.get(id=pk)
    context = {'object':Post_op.objects.get(id=pk)}
    if request.user != post.poster:
        messages.error(request, "You do not have the rights for this")
        return redirect('/posts/item_id=' + str(pk))
    if request.method == 'POST':
        post.delete()
        return redirect('/posts')
    return render(request, 'base_app/form_delete.html', context)

@login_required(login_url='Login')
def post_create_reply(request, pk):
    original = Post_op.objects.get(id=pk)
    context = {'original': original, 'form': Form_Post_reply()} # The op ID should be automatically given to the reply creator
    if request.method == 'POST':
        form = Form_Post_reply(request.POST) 
        if form.is_valid():
            filled = form.save(commit=False)
            filled.poster = request.user
            filled.original = original
            original.participants.add(request.user) # Automatically adding the replier as a 'participant'
            filled.save()
            return redirect('/posts/item_id=' + str(pk)) # Should return to the post page
    return render(request, 'base_app/posts_reply_form.html', context)

@login_required(login_url='Login')
def post_edit_reply(request, pk):
    post = Post_reply.objects.get(id=pk)
    context = {'post': post, 'form': Form_Post_reply(instance=post)}
    if request.user != post.poster:
        messages.error(request, "You do not have the rights for this")
        return redirect('/posts/item_id=' + str(post.original.id)) # Redirect back to the post page since replies don't have their own pages (yet)
    if request.method == 'POST':
        form = Form_Post_reply(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/posts/item_id=' + str(post.original.id))
        else:
            messages.error(request, "Something went wrong with the form")
    return render(request, 'base_app/posts_reply_form.html', context)

@login_required(login_url='Login')
def post_delete_reply(request, pk):
    post = Post_reply.objects.get(id=pk)
    op_id = post.original.id
    context = {'object':Post_reply.objects.get(id=pk)}
    if request.user != post.poster:
        messages.error(request, "You do not have the rights for this")
        return redirect('/posts/item_id=' + str(op_id))
    if request.method == 'POST':
        post.delete()
        return redirect('/posts/item_id=' + str(op_id))
    return render(request, 'base_app/form_delete.html', context)