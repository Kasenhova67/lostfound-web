from django.urls import path
from .views import (
    ItemLostListCreateView, ItemLostDetailView,
    ItemFoundListCreateView, ItemFoundDetailView,
    ProfileView, SearchView
)

urlpatterns = [
    path('lost/', ItemLostListCreateView.as_view(), name='api-lost-list'),
    path('lost/<int:pk>/', ItemLostDetailView.as_view(), name='api-lost-detail'),
    
    path('found/', ItemFoundListCreateView.as_view(), name='api-found-list'),
    path('found/<int:pk>/', ItemFoundDetailView.as_view(), name='api-found-detail'),
    
    path('profile/', ProfileView.as_view(), name='api-profile'),
    
    path('search/', SearchView.as_view(), name='api-search'),
]
