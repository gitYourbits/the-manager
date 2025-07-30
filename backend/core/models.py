from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class GlobalKnowledgeDocument(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='global_kb/')
    file_type = models.CharField(max_length=20, choices=[('pdf', 'PDF'), ('docx', 'DOCX'), ('txt', 'TXT'), ('other', 'Other')], default='other')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    # For future: store Qdrant vector id or embedding reference
    vector_id = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.title

# Signal to delete Qdrant vectors when global doc is deleted
@receiver(post_delete, sender=GlobalKnowledgeDocument)
def delete_global_vectors(sender, instance, **kwargs):
    from .services.qdrant_client import delete_vectors_by_doc_id
    if instance.id:
        delete_vectors_by_doc_id(str(instance.id), collection='global_kb')

class PersonalKnowledgeDocument(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personal_documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='personal_kb/')
    file_type = models.CharField(max_length=20, choices=[('pdf', 'PDF'), ('docx', 'DOCX'), ('txt', 'TXT'), ('other', 'Other')], default='other')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    vector_id = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.owner.email})"

# Signal to delete Qdrant vectors when personal doc is deleted
@receiver(post_delete, sender=PersonalKnowledgeDocument)
def delete_personal_vectors(sender, instance, **kwargs):
    from .services.qdrant_client import delete_vectors_by_doc_id
    if instance.id:
        delete_vectors_by_doc_id(str(instance.id), collection='personal_kb')

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    started_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"Conversation {self.id} ({self.user.email})"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=32, choices=[('user', 'User'), ('ai', 'AI')])
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    context = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.sender} @ {self.timestamp}: {self.text[:30]}..."
