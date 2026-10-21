from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from .models import InvoiceAuditRecord
from .serializers import InvoiceAuditRecordSerializer

class InvoiceAuditRecordViewSet(viewsets.ModelViewSet):
    """
    Unified Enterprise CRUD Engine for DocuVerify AI.
    Automatically handles:
    - POST   /api/audits/     -> Create an audit
    - GET    /api/audits/     -> List all audits for the user
    - GET    /api/audits/{id}/ -> Retrieve specific audit details
    - PUT    /api/audits/{id}/ -> Fully update an audit record
    - DELETE /api/audits/{id}/ -> Remove an audit record from history
    """
    serializer_class = InvoiceAuditRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Security Isolation Layer: Overrides the default database lookup to 
        ensure a user can ONLY view, update, or delete their own data records.
        """
        return InvoiceAuditRecord.objects.filter(owner=self.request.user).order_by('-uploaded_at')

    def perform_create(self, serializer):
        """
        Intercepts the creation pipeline to run our core Python logic 
        and calculate financial totals before writing to the database.
        """
        # 1. Pull validated data from our input boundaries
        subtotal_extracted = Decimal(str(serializer.validated_data.get('extracted_subtotal', '0.00')))
        total_extracted = Decimal(str(serializer.validated_data.get('extracted_total', '0.00')))
        
        # 2. Financial Integrity Engine (Layman-verified logic)
        tax_factor = Decimal('0.10')  # 10% base workspace profile calculation
        computed_subtotal = subtotal_extracted
        computed_total = computed_subtotal * (Decimal('1.00') + tax_factor)
        
        # 3. Delta Variance Analysis using absolute math absolute guard abs()
        is_total_valid = abs(computed_total - total_extracted) < Decimal('0.01')
        
        # 4. Resolve system audit states
        if is_total_valid:
            final_status = 'VERIFIED'
            system_log = "Verification complete: Data matrix is balanced."
        else:
            final_status = 'FLAGGED'
            system_log = f"Discrepancy: Stated total was {total_extracted}, calculation expected {computed_total}."
            
        # 5. Commit record securely with owner association
        serializer.save(
            owner=self.request.user,
            processing_status=final_status,
            computed_subtotal=computed_subtotal,
            computed_total=computed_total,
            system_flags_summary=system_log
        )
