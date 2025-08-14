from django.contrib import admin
from .models import Account, Transaction, Category


class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "account_name", "user", "account_balance")

    list_filter = ("account_created_at",)

    search_fields = ("account_name__icontains", "user__username__icontains")


class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "account",
        "user",
        "transaction_type",
        "transaction_amount",
        "transaction_category",
        "transaction_description",
        "transaction_created_at",
    )

    list_filter = (
        "transaction_type",
        "transaction_category",
        "transaction_created_at",
    )

    search_fields = (
        "transaction_description__icontains",
        "transaction_category__category_name__icontains",
        "user__username__icontains",
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name", "user")

    search_fields = ("category_name__icontains", "user__username__icontains")


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category, CategoryAdmin)
