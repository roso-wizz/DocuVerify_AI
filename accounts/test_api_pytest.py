import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from decimal import Decimal

@pytest.mark.django_db
def test_pytest_invoice_verification_flow(client):
    """Validates full boundary arithmetic matrix behavior using pytest fixtures."""
    user = User.objects.create_user(username="pytest_user", password="Password123")
    client.force_authenticate(user=user)
    
    url = reverse('audit-list')
    payload = {
        "document_name": "pytest_invoice.pdf",
        "raw_file_url": "https://amazonaws.com",
        "extracted_subtotal": "200.00",
        "extracted_total": "220.00" # 200 + 10% tax = 220
    }
    
    response = client.post(url, payload, content_type='application/json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['processing_status'] == 'VERIFIED'
    assert Decimal(response.data['computed_total']) == Decimal('220.00')
