from django.urls import path

from . import views
from auction import views as vi

app_name = 'main'
urlpatterns = [
    # path('', views.IndeView.as_view(), name='index'),
    path('',views.index, name='index'),
    # path('<int:id>/', vi.detail, name='detail')
    ]