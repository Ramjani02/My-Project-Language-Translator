from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('translate/', views.translate_view, name='translate'),
    path('chat/', views.chat_view, name='chat'),
    path('logout/', views.logout_view, name='logout'),
]
