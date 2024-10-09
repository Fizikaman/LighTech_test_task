from django.contrib.auth.models import User
from django.db import models


class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    amount = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.amount} копеек"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class BalanceTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
        ('transfer_in', 'Transfer In'),
        ('transfer_out', 'Transfer Out'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    related_user = models.ForeignKey(User, null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='related_transactions')

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount} копеек"

    class Meta:
        verbose_name = "Операция по балансу"
        verbose_name_plural = "Операции по балансу"
