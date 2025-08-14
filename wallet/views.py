from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction as db_transaction
from django.contrib.auth.models import User
from .models import Account, Category, Transaction
from .serializers import (
    AccountSerializer,
    CategorySerializer,
    TransactionSerializer,
    TransferSerializer,
    UserSerializer,
)
from .permissions import IsOwner


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwner()]


class AccountViewSet(viewsets.ModelViewSet):

    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class TransactionViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user)

    def perform_create(self, serializer):
        """
        Creates a new transaction and updates the account balance.
        Validation for a positive amount is now handled by the serializer.
        """
        # Ensure the account belongs to the authenticated user.
        # This is a critical security check.
        try:
            account = Account.objects.get(
                id=self.request.data.get("account"), user=self.request.user
            )
        except Account.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "account": "Invalid account ID or you do not have permission to access it."
                }
            )

        transaction_amount = serializer.validated_data.get("transaction_amount")
        transaction_type = serializer.validated_data.get("transaction_type")

        # Check for insufficient funds only if it's an expense.
        if (
            transaction_type == "expense"
            and (account.account_balance - transaction_amount) < 0
        ):
            raise serializers.ValidationError(
                {
                    "transaction_amount": "Insufficient funds. This transaction would result in a negative balance."
                }
            )

        # Now that all checks have passed, save the transaction and update the balance.
        transaction = serializer.save(user=self.request.user, account=account)

        if transaction.transaction_type == "income":
            account.account_balance += transaction_amount
        elif transaction.transaction_type == "expense":
            account.account_balance -= transaction_amount

        account.save()

    @action(detail=False, methods=["post"], serializer_class=TransferSerializer)
    def transfer(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender_account = serializer.validated_data["sender_account"]
        recipient_account = serializer.validated_data["recipient_account"]
        recipient_user = recipient_account.user

        # The amount is now guaranteed to be positive by the serializer.
        transaction_amount = serializer.validated_data["transaction_amount"]

        # Ensure the sender has enough funds.
        if sender_account.account_balance < transaction_amount:
            raise serializers.ValidationError(
                {"transaction_amount": "Insufficient funds."}
            )

        # Use a database transaction to ensure both updates happen together.
        with db_transaction.atomic():
            # Create a transaction for the sender (expense)
            Transaction.objects.create(
                user=request.user,
                account=sender_account,
                transaction_type="expense",
                transaction_amount=transaction_amount,
                transaction_description=f"Transfer to {recipient_user.username}",
            )

            # Update sender's balance
            sender_account.account_balance -= transaction_amount
            sender_account.save()

            # Create a transaction for the recipient (income)
            Transaction.objects.create(
                user=recipient_user,
                account=recipient_account,
                transaction_type="income",
                transaction_amount=transaction_amount,
                transaction_description=f"Transfer from {request.user.username}",
            )

            # Update recipient's balance
            recipient_account.account_balance += transaction_amount
            recipient_account.save()

        return Response({"status": "transfer successful"}, status=status.HTTP_200_OK)
