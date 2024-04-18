from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('roger_man/', views.get_roger_lines),
    path('roger_man/item_id=<str:pk>/', views.get_roger_response),
]