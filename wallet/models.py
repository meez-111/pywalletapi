from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_account"
    )
    account_name = models.CharField(max_length=100, blank=False, null=False)
    account_balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    account_created_at = models.DateTimeField(auto_now_add=True)
    account_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s {self.account_name} Account"


class Category(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_category"
    )
    category_name = models.CharField(max_length=100, blank=False, null=False)
    is_income = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category_name} (by {self.user.username})"

    class Meta:
        unique_together = ("user", "category_name")


class Transaction(models.Model):
    TRANSACTION_TYPES = {"income": "Income", "expense": "Expense"}

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_transaction"
    )
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="account_transaction"
    )
    transaction_category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    transaction_amount = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2
    )
    transaction_description = models.CharField(max_length=255, blank=True, null=True)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    transaction_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.transaction_amount} on {self.transaction_created_at.strftime('%Y-%m-%d')}"
