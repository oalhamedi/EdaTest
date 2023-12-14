from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('results/', views.results, name='results'),
    path('contact/', views.contact, name='contact'),
]