from django.urls import path
from . import views

app_name = 'comptes'

urlpatterns = [
    path('register/', views.register, name='register'),
    path("", views.login_view, name="login"),
]