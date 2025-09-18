from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid

User = get_user_model()

class Branch(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=120)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Customer(models.Model):
    GENDER_CHOICES = [('M','Male'),('F','Female'),('O','Other')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    other_names = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=30, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    national_id_number = models.CharField(max_length=100, blank=True, help_text="NIN / SSN / Passport")
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='customers_created')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['national_id_number']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Address(models.Model):
    customer = models.ForeignKey(Customer, related_name='addresses', on_delete=models.CASCADE)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Nigeria')
    postal_code = models.CharField(max_length=20, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer}: {self.line1}, {self.city}"

class KycDocument(models.Model):
    DOC_TYPES = [('ID','ID'),('UTILITY','Utility Bill'),('PASSPORT','Passport'),('OTHER','Other')]
    customer = models.ForeignKey(Customer, related_name='kyc_documents', on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES)
    file = models.FileField(upload_to='kyc/%Y/%m/')
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Account(models.Model):
    ACCOUNT_TYPES = [('SAV','Savings'),('CUR','Current'),('FIX','Fixed Deposit')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, related_name='accounts', on_delete=models.CASCADE)
    account_number = models.CharField(max_length=34, unique=True)  # IBAN-ish size
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='SAV')
    currency = models.CharField(max_length=3, default='NGN')
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    opened_at = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.account_number} ({self.get_account_type_display()})"

class Transaction(models.Model):
    TXN_TYPES = [('DEP','Deposit'),('WDL','Withdrawal'),('TRF','Transfer'),('CHG','Charge')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE)
    txn_type = models.CharField(max_length=4, choices=TXN_TYPES)
    amount = models.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(0.01)])
    timestamp = models.DateTimeField(default=timezone.now)
    reference = models.CharField(max_length=120, blank=True)
    performed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.txn_type} {self.amount} on {self.account.account_number}"

class AuditLog(models.Model):
    ACTIONS = [('CREATE','CREATE'),('UPDATE','UPDATE'),('DELETE','DELETE')]
    id = models.BigAutoField(primary_key=True)
    content_type = models.CharField(max_length=200)
    object_id = models.CharField(max_length=200)
    action = models.CharField(max_length=10, choices=ACTIONS)
    performed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
