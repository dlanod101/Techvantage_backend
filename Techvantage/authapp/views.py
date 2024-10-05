from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from Techvantage.firebase_config import firebase_admin
from .models import FirebaseUser

@api_view(['POST'])
def decode_user_info(request):
    try:
        # Extract UID from request data
        uid = request.data.get("uid")
        
        if not uid:
            return Response({"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Decode UID to retrieve user information
        user_info = auth.get_user(uid)

        # Extract and save user information to the database
        user_data = {
            "uid": user_info.uid,
            "email": user_info.email,
            "display_name": user_info.display_name,
            "phone_number": user_info.phone_number,
            "photo_url": user_info.photo_url,
            "provider_id": user_info.provider_id,
        }

        # Check if user already exists and update or create a new user
        firebase_user, created = FirebaseUser.objects.update_or_create(
            uid=user_info.uid,
            defaults=user_data
        )

        if created:
            response_message = "User information created successfully."
        else:
            response_message = "User information updated successfully."

        return Response({
            "message": response_message,
            "user_data": user_data,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_user_info(request, uid):
    try:
        # Retrieve user information from the database
        user = FirebaseUser.objects.get(uid=uid)

        user_data = {
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "phone_number": user.phone_number,
            "photo_url": user.photo_url,
            "provider_id": user.provider_id,
        }

        return Response({"user_data": user_data}, status=status.HTTP_200_OK)

    except FirebaseUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


