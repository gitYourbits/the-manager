from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from .models import GlobalKnowledgeDocument, PersonalKnowledgeDocument, Conversation, Message

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_artist')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            is_artist=validated_data.get('is_artist', False)
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError(_('Invalid credentials'))
        if not user.is_active:
            raise serializers.ValidationError(_('User is inactive'))
        data['user'] = user
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'is_admin', 'is_artist')

class GlobalKnowledgeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalKnowledgeDocument
        fields = ['id', 'title', 'file', 'file_type', 'uploaded_at', 'metadata', 'vector_id']
        read_only_fields = ['id', 'uploaded_at', 'vector_id']

class PersonalKnowledgeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalKnowledgeDocument
        fields = ['id', 'owner', 'title', 'file', 'file_type', 'uploaded_at', 'metadata', 'vector_id']
        read_only_fields = ['id', 'owner', 'uploaded_at', 'vector_id']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'text', 'timestamp', 'context']
        read_only_fields = ['id', 'timestamp', 'context']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Conversation
        fields = ['id', 'user', 'started_at', 'title', 'messages']
        read_only_fields = ['id', 'started_at', 'messages', 'user'] 