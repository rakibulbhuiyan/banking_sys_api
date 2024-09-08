from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerListCreateApi.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', views.CustomerDetailsApi.as_view(), name='customer-detail'),
    path('accounts/', views.AccountListCreateApi.as_view(), name='account-list-create'),
    path('accounts/<int:pk>/', views.AccountDetailsApi.as_view(), name='account-detail'),
    path('transactions/', views.TransactionListCreateAPI.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', views.TransactionDetailApi.as_view(), name='transaction-detail'),
]
