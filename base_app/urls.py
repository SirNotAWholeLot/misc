from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home page'),
    path('roger_man', views.roger_man, name='Roger Man'),
    path('roger_man/<str:pk>/', views.roger_response, name='Roger Man - Response'),
    path('roger_man/create', views.roger_create_response, name='Roger Man - Create a new response'),
    path('todo', views.todo_list, name='To do - objectives'),
    path('todo/<str:pk>/', views.todo_obj, name='To do - phases'),
    path('posts', views.posts_list, name='User posts'),
    path('posts/<str:pk>/', views.posts_post, name='User post'),
    path('posts/create', views.post_create_op, name='Create a new post'),
    path('posts/<str:pk>/reply', views.post_create_reply, name='Reply to a post'),
]