from django.urls import path
from .views import admin_global_kb_upload
from .views import RegisterView, LoginView, UserProfileView, GlobalKnowledgeDocumentListCreateView, GlobalKnowledgeDocumentRetrieveDestroyView, PersonalKnowledgeDocumentListCreateView, PersonalKnowledgeDocumentRetrieveDestroyView, global_kb_semantic_search, personal_kb_semantic_search, suggest_consultancy, ConversationListCreateView, ConversationDetailView, MessageCreateView

urlpatterns = [
    path('global_kb_upload/', admin_global_kb_upload, name='admin_global_kb_upload'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]

urlpatterns += [
    path('global-kb/', GlobalKnowledgeDocumentListCreateView.as_view(), name='global-kb-list-create'),
    path('global-kb/<int:pk>/', GlobalKnowledgeDocumentRetrieveDestroyView.as_view(), name='global-kb-detail'),
]

urlpatterns += [
    path('personal-kb/', PersonalKnowledgeDocumentListCreateView.as_view(), name='personal-kb-list-create'),
    path('personal-kb/<int:pk>/', PersonalKnowledgeDocumentRetrieveDestroyView.as_view(), name='personal-kb-detail'),
]

urlpatterns += [
    path('global-kb/search/', global_kb_semantic_search, name='global-kb-semantic-search'),
    path('personal-kb/search/', personal_kb_semantic_search, name='personal-kb-semantic-search'),
]

urlpatterns += [
    path('consultancy/suggest/', suggest_consultancy, name='consultancy-suggest'),
]

urlpatterns += [
    path('chat/conversations/', ConversationListCreateView.as_view(), name='chat-conversation-list-create'),
    path('chat/conversations/<int:pk>/', ConversationDetailView.as_view(), name='chat-conversation-detail'),
    path('chat/messages/', MessageCreateView.as_view(), name='chat-message-create'),
] 