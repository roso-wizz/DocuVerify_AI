from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Extends the default Django User model to add specialized enterprise fields 
    for DocuVerify AI workspace owners and developers.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    api_quota_limit = models.IntegerField(default=1000, help_text="Maximum documents allowed per billing cycle.")
    documents_processed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return "Profile for %s (%s)" % (self.user.username, self.company_name or "Independent")


class InvoiceAuditRecord(models.Model):
    """
    Saves verification records for text extracted from documents.
    Optimized with explicit database indexing for ultra-fast dashboard queries.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending Processing'),
        ('VERIFIED', 'Verification Passed'),
        ('FLAGGED', 'Discrepancy Flagged'),
        ('FAILED', 'System Error'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="audit_records")
    document_name = models.CharField(max_length=255)
    raw_file_url = models.URLField(help_text="Secure cloud storage URL path for audit traces.")
    
    # db_index=True ensures that even with 10 million rows, sorting by status is instant
    processing_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING', db_index=True)
    
    # Explicit DecimalFields protect against dangerous floating-point money math bugs
    extracted_subtotal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    computed_subtotal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    extracted_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    computed_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    system_flags_summary = models.TextField(blank=True, help_text="JSON structured log of any absolute mismatches.")
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Record {self.id} | {self.document_name} | Status: {self.processing_status}"
