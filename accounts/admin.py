from django.contrib import admin
from .models import UserProfile, InvoiceAuditRecord

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(InvoiceAuditRecord)