from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # as_view() method for class-based generic views
    path('register/', views.register, name='register'),     # register is a regular view function
]