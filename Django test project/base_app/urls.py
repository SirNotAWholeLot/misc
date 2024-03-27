from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('', views.home, name='home'),
    path('roger_man/', views.roger_man, name='roger'),
    path('roger_man/item_id=<str:pk>/', views.roger_response, name='roger_response'),
    path('roger_man/create/', views.roger_create_response, name='roger_create'),
    path('todo/', views.todo_list, name='todo_list'),
    path('todo/item_id=<str:pk>/', views.todo_objective, name='todo_objective'),
    path('posts/', views.posts_list, name='post_list'),
    path('posts/item_id=<str:pk>/', views.posts_post, name='post_post'),
    path('posts/create/', views.post_create_op, name='post_create'),
    path('posts/item_id=<str:pk>/edit/', views.post_edit_op, name='post_edit'),
    path('posts/item_id=<str:pk>/reply/', views.post_create_reply, name='post_reply_create'),
    path('posts/item_id=<str:pk>/delete/', views.post_delete_op, name='post_delete'),
    path('posts/reply_id=<str:pk>/edit/', views.post_edit_reply, name='post_reply_edit'),
    path('posts/reply_id=<str:pk>/delete/', views.post_delete_reply, name='post_reply_delete'),
]