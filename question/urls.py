#coding: utf8

from django.urls import path, re_path

from . import views, views_register_user as views_User

urlpatterns = [
    re_path(r'^$', views.question, name='question'),
    re_path(r'^resposta/$', views.question_answer, name='question_answer'),
    re_path("cadastro/", views_User.register, name="cadastro"),

]