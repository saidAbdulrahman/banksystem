from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, AccountViewSet, TransactionViewSet
from django.urls import path, include
from . import views

app_name = "bank"
router = DefaultRouter()
router.register('customers', CustomerViewSet)
router.register('accounts', AccountViewSet)
router.register('transactions', TransactionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<uuid:pk>/', views.customer_detail, name='customer_detail'),

]
