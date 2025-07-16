from django.contrib import admin
from .models import User
from .models import GlobalKnowledgeDocument
from .models import PersonalKnowledgeDocument
from .models import Conversation, Message

admin.site.register(User)
admin.site.register(GlobalKnowledgeDocument)
admin.site.register(PersonalKnowledgeDocument)
admin.site.register(Conversation)
admin.site.register(Message)
