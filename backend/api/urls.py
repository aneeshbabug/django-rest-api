from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('api/auth/register/', views.RegisterBackendUserView.as_view(), name='register'),
    path('api/auth/token/',TokenObtainPairView.as_view(),name='gettoken'),
    path('api/auth/token/refresh/',TokenRefreshView.as_view(),name='tokenrefresh'),
    path('api/auth/logout/',TokenBlacklistView.as_view(),name='logout'),
    path('api/items/', views.ItemListCreateView.as_view(),name='item-list-create'),
    path('api/items/<int:id>/', views.ItemDetailView.as_view(), name='item-detail')
]