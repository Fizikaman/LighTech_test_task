from rest_framework import serializers


class AddBalanceSerializer(serializers.Serializer):
    """Сериализатор для добавления баланса"""
    amount = serializers.IntegerField(min_value=1)


class TransferBalanceSerializer(serializers.Serializer):
    """Сериализатор для трансфера денег"""
    amount = serializers.IntegerField(min_value=1)
    recipient_id = serializers.IntegerField()
