from rest_framework import serializers
from .models import ChatRoom, FirebaseUser, Membership, Message

class FirebaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseUser
        fields = ['uid', 'email', 'display_name']

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']

    def validate_name(self, value):
        if ChatRoom.objects.filter(name=value).exists():
            raise serializers.ValidationError("A chat room with this name already exists.")
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)  # To show sender email instead of just ID
    chat_room = serializers.StringRelatedField(read_only=True)  # To show chat room name instead of just ID

    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'sender', 'content', 'date_published']  # Fields to expose in the API
        read_only_fields = ['date_published']  # Make timestamp read-only since it is set automatically

class MembershipSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Show user email instead of ID
    chat_room = serializers.StringRelatedField(read_only=True)  # Show chat room name instead of ID

    class Meta:
        model = Membership
        fields = ['id', 'user', 'chat_room', 'joined_at']
        read_only_fields = ['joined_at']
