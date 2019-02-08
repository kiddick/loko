from django.urls import path

from . import views

app_name = 'ldate'
urlpatterns = [
    path('', views.index, name='index'),
    path('calc/', views.calc, name='calc'),
]
