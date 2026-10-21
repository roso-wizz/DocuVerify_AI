from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import InvoiceAuditRecord

class InvoiceAuditEngineTests(APITestCase):
    """
    Automated test matrix ensuring financial validation constraints and 
    IsAuthenticated security perimeters execute correctly.
    """
    def setUp(self):
        # Build sandboxed master user account credentials
        self.user = User.objects.create_user(username="testdev", password="SecurePassword123")
        self.url = reverse('audit-list') # Maps automatically to /api/audits/

    def test_verified_invoice_math_loop(self):
        """Validates that a mathematically sound invoice resolves to VERIFIED."""
        self.client.force_authenticate(user=self.user)
        payload = {
            "document_name": "valid_cloud_bill.pdf",
            "raw_file_url": "https://amazonaws.com",
            "extracted_subtotal": "150.00",
            "extracted_total": "165.00" # 150 + 10% tax = 165
        }
        response = self.client.post(self.url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['processing_status'], 'VERIFIED')
        self.assertEqual(InvoiceAuditRecord.objects.count(), 1)

    def test_tampered_invoice_flagged_safeguard(self):
        """Validates that a discrepancy automatically triggers a FLAGGED status via abs()."""
        self.client.force_authenticate(user=self.user)
        payload = {
            "document_name": "fraudulent_invoice.pdf",
            "raw_file_url": "https://amazonaws.com",
            "extracted_subtotal": "150.00",
            "extracted_total": "999.00" # Broken math
        }
        response = self.client.post(self.url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['processing_status'], 'FLAGGED')
        self.assertIn("Discrepancy", response.data['system_flags_summary'])

    def test_anonymous_traffic_blocked(self):
        """Ensures that unauthenticated traffic hits the security boundary shield."""
        payload = {"document_name": "leak.pdf", "raw_file_url": "https://leak.url"}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
