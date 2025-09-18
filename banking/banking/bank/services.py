from django.db import transaction
from .models import Account, Transaction

def deposit(account_id, amount, performed_by=None):
    with transaction.atomic():
        acc = Account.objects.select_for_update().get(pk=account_id)
        acc.balance += amount
        acc.save()
        return Transaction.objects.create(account=acc, txn_type='DEP', amount=amount, performed_by=performed_by)
