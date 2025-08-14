from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Account, Category, Transaction


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        user.set_password(validated_data["password"])

        user.save()

        return user


class AccountSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "user",
            "account_name",
            "account_created_at",
            "account_updated_at",
            "account_balance",
        ]
        read_only_fields = [
            "account_balance",
            "account_created_at",
            "account_updated_at",
        ]


class CategorySerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "user", "category_name", "is_income"]


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    transaction_category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "user",
            "account",
            "transaction_category",
            "transaction_description",
            "transaction_amount",
            "transaction_type",
            "transaction_created_at",
        ]
        read_only_fields = ["transaction_created_at"]

    def validate_transaction_amount(self, value):
        """
        Validates that the transaction amount is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Transaction amount must be a positive number."
            )
        return value


User = get_user_model()


class TransferSerializer(serializers.Serializer):
    recipient_username = serializers.CharField(max_length=150)
    recipient_account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all()
    )
    transaction_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    sender_account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())

    def validate_transaction_amount(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Transfer amount must be a positive number."
            )
        return value

    def validate(self, data):
        recipient_username = data.get("recipient_username")
        recipient_account = data.get("recipient_account")

        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"recipient_username": "Recipient user does not exist."}
            )

        if recipient_account.user != recipient:
            raise serializers.ValidationError(
                {
                    "recipient_account": "The recipient's account does not belong to the recipient user."
                }
            )

        return data
