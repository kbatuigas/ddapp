"""ddmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView
from manager import views as mviews

# Set the application namespace so Django can differentiate URL names
# between multiple applications (although we don't currently have this).
#
app_name = 'manager'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('manager/', include('manager.urls')),
    # Redirect base URL to our manager app view. Empty string '' implies '/'
    path('', RedirectView.as_view(url='manager/', permanent=True)),
    # Instead of Django's out of the box authentication views, we reference specific views
    # to have more control over URLs/templates. Don't forget to include the name parameter if you do this!
    path('account/login/', auth_views.LoginView.as_view(template_name='manager/login.html'), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(template_name='manager/logout.html'), name='logout'),
    path('account/', include('django.contrib.auth.urls')),    # Django's out of the box auth views
]
