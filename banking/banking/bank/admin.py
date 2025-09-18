from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, Address, Account, Transaction, KycDocument, Branch, AuditLog

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('code','name','phone')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','phone','national_id_number','is_active','created_at')
    search_fields = ('first_name','last_name','email','phone','national_id_number')
    list_filter = ('is_active','branch')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number','customer','account_type','balance','is_active')
    search_fields = ('account_number','customer__first_name','customer__last_name')
    list_filter = ('account_type','currency','is_active')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('txn_type','amount','account','timestamp','performed_by')
    search_fields = ('account__account_number','reference')
    list_filter = ('txn_type',)

@admin.register(KycDocument)
class KycDocAdmin(admin.ModelAdmin):
    list_display = ('customer','doc_type','uploaded_at','expiry_date')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('content_type','object_id','action','performed_by','created_at')
    readonly_fields = ('content_type','object_id','action','performed_by','summary','created_at')
