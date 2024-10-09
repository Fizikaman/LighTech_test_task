from django.urls import path
from .views import AddBalanceView, TransferBalanceView, GetBalanceView

urlpatterns = [
    path('balance/add/', AddBalanceView.as_view(), name='add-balance'),
    path('balance/transfer/', TransferBalanceView.as_view(), name='transfer-balance'),
    path('balance/', GetBalanceView.as_view(), name='get-balance'),
]