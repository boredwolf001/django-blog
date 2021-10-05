from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.shortcuts import render

from .views import dashboard, deleteArticle, newArticle, editArticle, allArticles, singleArticle, commentArticle, index

urlpatterns = [
	path('', index),
	path('dashboard', dashboard),
	path('articles', allArticles),
	path('articles/new', newArticle),
	path('articles/<id>', singleArticle),
	path('articles/edit/<id>', editArticle),
	path('articles/delete/<id>', deleteArticle),
	path('articles/comment/<id>', commentArticle),
]