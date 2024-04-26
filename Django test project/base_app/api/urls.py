from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.get_routes, name='api_routes'),
    path('roger_man/', views.get_roger_lines),
    path('roger_man/item_id=<str:pk>/', views.get_roger_response),
    path('roger_man/names/', views.get_roger_line_names),
]

urlpatterns = format_suffix_patterns(urlpatterns)