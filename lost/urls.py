from django.urls import path
from . import views

app_name = 'lost'

urlpatterns = [
    path('', views.lost_view, name='lost_list'),
    path('report/', views.lost_enter, name='enter_lost'),
]