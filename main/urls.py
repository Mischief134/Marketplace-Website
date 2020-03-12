from django.urls import path

from . import views


app_name = 'main'
urlpatterns = [
    # path('', views.IndeView.as_view(), name='index'),
    path('',views.index, name='index')
    ]