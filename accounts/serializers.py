from rest_framework import serializers
from .models import InvoiceAuditRecord

class InvoiceAuditRecordSerializer(serializers.ModelSerializer):
    """
    Data boundary layout that validates incoming HTTP payloads
    and maps them safely to the Django database ORM layer.
    """
    # Explicitly mark calculated values as read-only so the client cannot forge records
    processing_status = serializers.CharField(read_only=True)
    computed_subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    computed_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    system_flags_summary = serializers.CharField(read_only=True)

    class Meta:
        model = InvoiceAuditRecord
        fields = [
            'id',
            'document_name',
            'raw_file_url',
            'processing_status',
            'extracted_subtotal',
            'computed_subtotal',
            'extracted_total',
            'computed_total',
            'system_flags_summary',
            'uploaded_at'
        ]
