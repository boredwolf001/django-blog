"""django_markdown_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import django
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.shortcuts import render

from blog.models import Profile


def register(request):
    if request.method == 'POST':
        errors = []
        if request.POST['name'] == '' or request.POST['password'] == '':
            errors.append('Please fill required fileds')
            return render(request, 'registration/register.html', {'errors': errors})
        if len(request.POST['password']) < 6:
            if 'Please fill required fileds' not in errors:
                errors.append('Password must be at least 6 charachters long')
            return render(request, 'registration/register.html', {'errors': errors})
        if request.POST['password'] != request.POST['confpassword']:
            if 'Please fill required fileds' not in errors:
                errors.append('Passwords didn\'t match')
            return render(request, 'registration/register.html', {'errors': errors})

        else:
            try:
                user = User.objects.create_user(
                    request.POST['name'], request.POST['email'], request.POST['password'])
                user.save()
                profile = Profile.objects.create(user=user)
                profile.setProfile()
                profile.save()
                return HttpResponseRedirect('/auth/login')
            except django.db.IntegrityError:
                errors.append('User already exists')
                return render(request, 'registration/register.html', {'errors': errors})
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard')
        return render(request, 'registration/register.html')


def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/auth/login')
    try:
        user = User.objects.get(username=request.user.username)
        return render(request, 'pages/profile.html', {'profile': user})
    except Exception as e:
        print(e)


def update(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        try:
            user = User.objects.get(username=request.user.username)
            user.username = username
            user.email = email
            user.save()
        except Exception as e:
            print(e)

        return HttpResponseRedirect('/profile')
    else:
        return HttpResponseRedirect('/')


urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('profile/', profile),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/register', register),
    path('auth/update', update),
    path('auth/login', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
]
