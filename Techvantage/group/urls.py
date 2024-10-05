from django.urls import path
from .views import *

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
     # CRUD for ChatRoom
    path('chat_rooms/', ChatRoomListCreateView.as_view(), name='chat_room_list_create'),  # List & Create Chat Rooms
    path('chat_rooms/<int:pk>/', ChatRoomRetrieveUpdateDestroyView.as_view(), name='chat_room_detail'),  # CRUD on specific Chat Room
    path('chatrooms/<int:chat_room_id>/remove_member/', RemoveMemberView.as_view(), name='remove_member'),

    # CRUD for Message
    path('messages/', MessageListCreateView.as_view(), name='message_list_create'),  # List & Create Messages
    path('messages/<int:pk>/', MessageRetrieveUpdateDestroyView.as_view(), name='message_detail'),  # CRUD on specific Message

    # CRUD for Membership
    path('memberships/', MembershipListCreateView.as_view(), name='membership_list_create'),  # List & Create Memberships
    path('memberships/<int:pk>/', MembershipRetrieveUpdateDestroyView.as_view(), name='membership_detail'),  # CRUD on specific Membership
    

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
