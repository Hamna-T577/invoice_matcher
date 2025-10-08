

# Create your models here.


from django.db import models

class Document(models.Model):
    DOC_TYPES = [
        ('invoice', 'Invoice'),
        ('po', 'Purchase Order'),
    ]
    doc_type = models.CharField(max_length=10, choices=DOC_TYPES)
    file = models.FileField(upload_to='uploads/')
    original_name = models.CharField(max_length=255, blank=True)
    extracted = models.JSONField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_name} ({self.doc_type})"
