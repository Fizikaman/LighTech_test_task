from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from LayTech_test_task.swagger_schema import TOKENS_PARAMETER
from .models import UserBalance, BalanceTransaction
from .serializers import AddBalanceSerializer, TransferBalanceSerializer


class AddBalanceView(APIView):
    """Вьюха для пополнения баланса"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary='Метод для пополнения баланса',
                         request_body=AddBalanceSerializer,
                         **TOKENS_PARAMETER)
    def post(self, request):
        serializer = AddBalanceSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            user = request.user
            with transaction.atomic():
                user_balance, _ = UserBalance.objects.select_for_update().get_or_create(user=user)
                user_balance.amount += amount
                user_balance.save()

                BalanceTransaction.objects.create(
                    user=user,
                    transaction_type='credit',
                    amount=amount,
                    description='Пополнение баланса'
                )
            return Response({'status': 'Баланс успешно пополнен.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferBalanceView(APIView):
    """Вьюха для перевода денег другому пользователю"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary='Метод для перевода денег другому пользователю',
                         request_body=TransferBalanceSerializer,
                         **TOKENS_PARAMETER)
    def post(self, request):
        serializer = TransferBalanceSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            recipient_id = serializer.validated_data['recipient_id']

            try:
                recipient = User.objects.get(id=recipient_id)
            except User.DoesNotExist:
                return Response({'error': 'Получатель не найден.'}, status=status.HTTP_404_NOT_FOUND)

            if recipient == request.user:
                return Response({'error': 'Нельзя перевести средства самому себе.'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                sender_balance = UserBalance.objects.select_for_update().get(user=request.user)
                if sender_balance.amount < amount:
                    return Response({'error': 'Недостаточно средств.'}, status=status.HTTP_400_BAD_REQUEST)

                recipient_balance, _ = UserBalance.objects.select_for_update().get_or_create(user=recipient)

                sender_balance.amount -= amount
                sender_balance.save()

                recipient_balance.amount += amount
                recipient_balance.save()

                # Запись транзакций
                BalanceTransaction.objects.create(
                    user=request.user,
                    transaction_type='transfer_out',
                    amount=amount,
                    description=f'Перевод пользователю {recipient.username}',
                    related_user=recipient
                )

                BalanceTransaction.objects.create(
                    user=recipient,
                    transaction_type='transfer_in',
                    amount=amount,
                    description=f'Получен перевод от {request.user.username}',
                    related_user=request.user
                )

            return Response({'status': 'Перевод выполнен успешно.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetBalanceView(APIView):
    """Вьюха для получения текущего баланса"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary='Метод для получения текущего баланса',
                         **TOKENS_PARAMETER)
    def get(self, request):
        user_balance, _ = UserBalance.objects.get_or_create(user=request.user)
        amount_in_rubles = user_balance.amount / 100.0
        return Response({'balance': amount_in_rubles}, status=status.HTTP_200_OK)