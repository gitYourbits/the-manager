from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from .models import GlobalKnowledgeDocument
from .serializers import GlobalKnowledgeDocumentSerializer
from .models import PersonalKnowledgeDocument
from .serializers import PersonalKnowledgeDocumentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
from .services.ingestion import embed_text
from .services.qdrant_client import search_vectors
from .services.ai_service import ai_service
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin

class GlobalKnowledgeDocumentListCreateView(generics.ListCreateAPIView):
    queryset = GlobalKnowledgeDocument.objects.all().order_by('-uploaded_at')
    serializer_class = GlobalKnowledgeDocumentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

class GlobalKnowledgeDocumentRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = GlobalKnowledgeDocument.objects.all()
    serializer_class = GlobalKnowledgeDocumentSerializer
    permission_classes = [IsAdminOrReadOnly]

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class PersonalKnowledgeDocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = PersonalKnowledgeDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PersonalKnowledgeDocument.objects.filter(owner=self.request.user).order_by('-uploaded_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PersonalKnowledgeDocumentRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = PersonalKnowledgeDocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return PersonalKnowledgeDocument.objects.filter(owner=self.request.user)

@api_view(['POST'])
@permission_classes([AllowAny])
def global_kb_semantic_search(request):
    query = request.data.get('query')
    if not query:
        return Response({'error': 'Query is required.'}, status=400)
    embedding = embed_text([query])[0]
    results = search_vectors(embedding, collection='global_kb', top=5)
    return Response(results)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def personal_kb_semantic_search(request):
    query = request.data.get('query')
    if not query:
        return Response({'error': 'Query is required.'}, status=400)
    embedding = embed_text([query])[0]
    # Filter by user_id in Qdrant
    user_id = request.user.id
    results = search_vectors(embedding, collection='personal_kb', top=5)
    # Filter results to only those with matching user_id in payload
    filtered = [r for r in results.get('result', []) if r['payload'].get('user_id') == user_id]
    return Response({'result': filtered})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def suggest_consultancy(request):
    user = request.user
    # Example: fetch recent personal KB docs, analyze trends, suggest actions
    from .models import PersonalKnowledgeDocument
    recent_docs = PersonalKnowledgeDocument.objects.filter(owner=user).order_by('-uploaded_at')[:10]
    # Placeholder: In production, use semantic search, trend analysis, etc.
    suggestions = []
    if not recent_docs:
        suggestions.append("Upload documents to get personalized suggestions.")
    else:
        suggestions.append("Review your most recent uploads for new opportunities.")
        # Example: warn if user uploads many docs but doesn't act
        if len(recent_docs) >= 5:
            suggestions.append("You have uploaded several documents recently. Consider setting clear goals for the week.")
        # Placeholder for more advanced logic
    return Response({
        'suggestions': suggestions,
        'recent_docs': [doc.title for doc in recent_docs]
    })

class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user).order_by('-started_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ConversationDetailView(generics.RetrieveAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.all()

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        conversation = Conversation.objects.get(id=self.request.data['conversation'], user=self.request.user)
        # Save user message
        msg = serializer.save(conversation=conversation, sender='user')
        # Retrieve last N messages for context
        context_msgs = Message.objects.filter(conversation=conversation).order_by('-timestamp')[:10][::-1]
        context_texts = [m.text for m in context_msgs]
        # Generate AI response using RAG
        ai_response = ai_service.generate_response(
            user_message=msg.text,
            conversation_history=context_texts,
            user_id=self.request.user.id
        )
        # Save AI message
        Message.objects.create(conversation=conversation, sender='ai', text=ai_response, context={"history": context_texts})
