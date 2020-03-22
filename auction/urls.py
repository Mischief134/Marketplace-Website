from django.urls import path

from . import views


app_name = 'main'
urlpatterns = [
    # path('', views.IndeView.as_view(), name='index'),
    path('',views.list_of_products, name='list_of_products')

    ]