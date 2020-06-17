from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # as_view() method for class-based generic views
    path('character/<int:pk>', views.PcDetailView.as_view(), name='character-detail'),
    path('characters/', views.PcListView.as_view(), name='characters'),
    path('characters/create/', views.PcCreate.as_view(), name='character-create'),
    path('register/', views.register, name='register'),     # register is a regular view function

]