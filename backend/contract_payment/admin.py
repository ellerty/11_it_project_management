from django.contrib import admin
from .models import Contract, Payment, Invoice

# Register your models here.
admin.site.register(Contract)
admin.site.register(Payment)
admin.site.register(Invoice)
