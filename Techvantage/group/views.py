from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from django.http import JsonResponse
from .models import ChatRoom, Message, Membership, FirebaseUser
from .serializers import ChatRoomSerializer, MessageSerializer, MembershipSerializer

# CRUD for ChatRoom
class ChatRoomListCreateView(generics.ListCreateAPIView):
    """
    `POST` - Creates a new Chat Room
    `GET` - Lists out all existing Chat Rooms
    """
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


class ChatRoomRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

# CRUD for Message
class MessageListCreateView(generics.ListCreateAPIView):
    """
    `POST` - Creates a new message
    `GET` - Lists out all existing messages in a Chat Room
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        # Optional filtering by chat_room_id
        chat_room_id = self.request.query_params.get('chat_room_id')
        if chat_room_id:
            return self.queryset.filter(chat_room__id=chat_room_id)
        return self.queryset

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        chat_room_id = self.request.data.get('chat_room_id')

        # Check if the user is a member of the chat room
        if not Membership.objects.filter(user__id=user_id, chat_room__id=chat_room_id).exists():
            raise PermissionDenied("User is not a member of this chat room")

        # Save the message if user is a member
        user = FirebaseUser.objects.get(pk=user_id)
        chat_room = ChatRoom.objects.get(pk=chat_room_id)
        serializer.save(sender=user, chat_room=chat_room)

class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

# CRUD for Membership
class MembershipListCreateView(generics.ListCreateAPIView):
    """
    `POST` - Adds a specified member to a Chat Room
    `GET` - Lists out all existing members of an existing Chat Room
    """
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    def get_queryset(self):
        # Optional filtering by user or chat_room
        user_id = self.request.query_params.get('user_id')
        chat_room_id = self.request.query_params.get('chat_room_id')
        queryset = self.queryset
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        if chat_room_id:
            queryset = queryset.filter(chat_room__id=chat_room_id)
        return queryset

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        chat_room_id = self.request.data.get('chat_room_id')
        
        # Fetch user and chat room instances
        user = FirebaseUser.objects.get(pk=user_id)
        chat_room = ChatRoom.objects.get(pk=chat_room_id)
        
        # Save the new membership
        serializer.save(user=user, chat_room=chat_room)


class MembershipRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

class RemoveMemberView(generics.DestroyAPIView):
    """
    `Removes a User from an existing Chat Room`
    """
    def delete(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')  # User ID of the member to remove
        chat_room_id = kwargs.get('chat_room_id')  # Chat room ID from the URL

        try:
            # Retrieve the specific membership entry
            membership = Membership.objects.get(user_id=user_id, chat_room_id=chat_room_id)
            membership.delete()  # Remove the member from the chatroom

            return JsonResponse({'message': 'Member removed successfully.'}, status=status.HTTP_204_NO_CONTENT)

        except Membership.DoesNotExist:
            return JsonResponse({'error': 'Membership not found.'}, status=status.HTTP_404_NOT_FOUND)