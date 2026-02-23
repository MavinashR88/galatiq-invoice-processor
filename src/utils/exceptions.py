class InvoiceProcessingError(Exception):
    pass


class ExtractionError(InvoiceProcessingError):
    pass


class ValidationError(InvoiceProcessingError):
    pass


class ApprovalError(InvoiceProcessingError):
    pass


class PaymentError(InvoiceProcessingError):
    pass