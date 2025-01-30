from django.urls import path
from . import views

app_name='weatherapp'

urlpatterns=[
    path('',views.home,name='home'),
    path('results',views.results,name='results'),
]   