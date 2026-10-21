from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceAuditRecordViewSet

# Initialize the automated API routing matrix
router = DefaultRouter()
router.register(r'audits', InvoiceAuditRecordViewSet, basename='audit')

urlpatterns = [
    # Include all auto-generated CRUD paths directly
    path('', include(router.urls)),
]
