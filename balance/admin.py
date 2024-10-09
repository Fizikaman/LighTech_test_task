from django.contrib import admin

from balance.models import UserBalance, BalanceTransaction

admin.site.register(UserBalance)
admin.site.register(BalanceTransaction)
