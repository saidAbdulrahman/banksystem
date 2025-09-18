from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.db import models
from .models import Customer

# HTML views
def customer_list(request):
    q = request.GET.get('q','')
    qs = Customer.objects.all()
    if q:
        qs = qs.filter(
            models.Q(first_name__icontains=q) |
            models.Q(last_name__icontains=q) |
            models.Q(phone__icontains=q) |
            models.Q(national_id_number__icontains=q)
        )
    return render(request, 'bank/customer_list.html', {'customers': qs})

def customer_detail(request, pk):
    c = get_object_or_404(Customer, pk=pk)
    return render(request, 'bank/customer_detail.html', {'customer': c})

from rest_framework import viewsets, permissions
from .models import Customer, Account, Transaction
from .serializers import CustomerSerializer, AccountSerializer, TransactionSerializer

class IsBankStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().select_related('branch')
    serializer_class = CustomerSerializer
    permission_classes = [IsBankStaff]

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().select_related('customer')
    serializer_class = AccountSerializer
    permission_classes = [IsBankStaff]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().select_related('account')
    serializer_class = TransactionSerializer
    permission_classes = [IsBankStaff]
