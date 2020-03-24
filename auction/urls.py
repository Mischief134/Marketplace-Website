from django.urls import path

from . import views


app_name = 'auction'
urlpatterns = [
    # path('', views.IndeView.as_view(), name='index'),
    # path('',views.list_of_products, name='list_of_products')
    path('<int:id>/', views.detail, name='detail')
    ]