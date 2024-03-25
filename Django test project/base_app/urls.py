from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='Login'),
    path('logout/', views.logout_page, name='Logout'),
    path('register/', views.register_page, name='Register'),
    path('', views.home, name='Home page'),
    path('roger_man/', views.roger_man, name='Roger Man'),
    path('roger_man/item_id=<str:pk>/', views.roger_response, name='Roger Man - Response'),
    path('roger_man/create/', views.roger_create_response, name='Roger Man - Create a new response'),
    path('todo/', views.todo_list, name='To do - objectives'),
    path('todo/item_id=<str:pk>/', views.todo_obj, name='To do - phases'),
    path('posts/', views.posts_list, name='User posts'),
    path('posts/item_id=<str:pk>/', views.posts_post, name='User post'),
    path('posts/create/', views.post_create_op, name='Create a new post'),
    path('posts/item_id=<str:pk>/edit/', views.post_edit_op, name='Edit post'),
    path('posts/item_id=<str:pk>/reply/', views.post_create_reply, name='Reply to a post'),
    path('posts/item_id=<str:pk>/delete/', views.post_delete_op, name='Delete post'),
    path('posts/reply_id=<str:pk>/edit/', views.post_edit_reply, name='Edit reply'),
    path('posts/reply_id=<str:pk>/delete/', views.post_delete_reply, name='Delete reply'),
]