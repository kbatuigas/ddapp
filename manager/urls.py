from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # as_view() method for class-based generic views
    path('character/<int:pk>', views.PcDetailView.as_view(), name='character-detail'),
    path('character/<int:pk>/edit/', views.PcUpdate.as_view(), name='character-edit'),
    path('characters/', views.PcListView.as_view(), name='characters'),

    path('characters/create/', views.PcCreate.as_view(), name='character-create'),
    # path('campaigns/', views.PcListView.as_view(), name='characters'),
    path('campaigns/signup/', views.CampaignSignUp.as_view(), name='campaign-signup'),
    path('campaigns/create/', views.CampaignCreate.as_view(), name='campaign-create'),
    path('register/', views.register, name='register'),     # register is a regular view function

]