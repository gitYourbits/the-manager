from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GlobalKnowledgeDocument, PersonalKnowledgeDocument
from .services.ingestion import ingest_document
from .services.qdrant_client import upsert_vectors

# Utility to get file type from model instance

def read_file_content(file_field):
    file_field.seek(0)
    return file_field.read().decode('utf-8')

@receiver(post_save, sender=GlobalKnowledgeDocument)
def ingest_global_kb(sender, instance, created, **kwargs):
    if not created:
        return
    vectors = ingest_document(
        instance.file,
        instance.file_type,
        doc_metadata={
            'document_id': instance.id,
            'title': instance.title,
            'file_type': instance.file_type
        },
        is_global=True
    )
    upsert_vectors(vectors, collection='global_kb')

@receiver(post_save, sender=PersonalKnowledgeDocument)
def ingest_personal_kb(sender, instance, created, **kwargs):
    if not created:
        return
    vectors = ingest_document(
        instance.file,
        instance.file_type,
        doc_metadata={
            'document_id': instance.id,
            'title': instance.title,
            'file_type': instance.file_type
        },
        user_id=instance.owner.id,
        is_global=False
    )
    upsert_vectors(vectors, collection='personal_kb') 