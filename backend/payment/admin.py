from django.contrib import admin
from .models import PaymentMethod, Currency, Transaction, PaymentAccount, Invoice, Refund, WalletBalance

admin.site.register(PaymentMethod)
admin.site.register(Currency)
admin.site.register(Transaction)
admin.site.register(PaymentAccount)
admin.site.register(Invoice)
admin.site.register(Refund)
admin.site.register(WalletBalance)
