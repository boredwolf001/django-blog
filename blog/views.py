from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone, dateformat
from django.http import HttpResponseRedirect, Http404

from .models import Article
print()

def index(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/dashboard')
	return render(request, 'pages/home.html')

def dashboard(request):
	articles = []
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/auth/login')
	try:
		user = User.objects.get(username=request.user.username)
		articles = user.article_set.all()
	except:
		pass
	return render(request, 'pages/dashboard.html', {'articles': articles})

def allArticles(request):
	try:
		articles = Article.objects.all()
		return render(request, 'articles/all.html', {'articles': articles})
	except Exception as e:
		print(e)
		return render(request, 'articles/all.html')

def singleArticle(request, id):
	try:
		article = Article.objects.get(pk=id)
		article.views += 1
		article.save()
		return render(request, 'articles/single.html', {'article': article})
	except:
		pass

def newArticle(request):
	if request.method == 'POST':
		user = User.objects.get(username=request.user.username)

		title = request.POST['title']
		description = request.POST['description']
		body = request.POST['body']

		article = Article.objects.create(user=user, title=title, description=description, body=body)
		article.save()

		return HttpResponseRedirect('/dashboard')

	else:
		return render(request, 'articles/new.html')

def editArticle(request, id):
	if request.method == 'POST':
		title = request.POST['title']
		description = request.POST['description']
		body = request.POST['body']

		try:
			article = Article.objects.get(pk=id)
			article.title = title
			article.description = description
			article.body = body
			article.save()

			return HttpResponseRedirect('/dashboard')
		except:
			return HttpResponseRedirect('/dashboard')
		
	else:
		try:
			article = Article.objects.get(pk=id)
			if not article.user.username == request.user.username:
				return HttpResponseRedirect('/articles')
		except:
			return HttpResponseRedirect('/dashboard')
		return render(request, 'articles/edit.html' , {'values': article})

def deleteArticle(request, id):
	article = Article.objects.get(pk=id)
	if not article.user.username == request.user.username:
				return HttpResponseRedirect('/articles')
	article.delete()

	return HttpResponseRedirect('/dashboard')

def commentArticle(request, id):
	return HttpResponseRedirect('/')
