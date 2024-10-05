# your_app/middlewares.py

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from firebase_admin import auth
from django.contrib.auth.models import AnonymousUser  # Import AnonymousUser
from .models import FirebaseUser

class FirebaseAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate requests using Firebase.
    """
    def process_request(self, request):
        # Get the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if not auth_header:
            request.user = AnonymousUser()  # Assign AnonymousUser if no Authorization header
            return None

        # Expect the token to be in the format: 'Bearer <token>'
        try:
            id_token = auth_header.split(' ')[1]
        except IndexError:
            return JsonResponse({'error': 'Invalid Authorization header format'}, status=400)

        try:
            # Verify the ID token with Firebase Admin SDK
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token.get('uid')

            # Retrieve or create a FirebaseUser in the database using the UID
            user, _ = FirebaseUser.objects.get_or_create(uid=uid)

            # Attach the FirebaseUser instance to the request
            request.user = user

        except Exception as e:
            # In case of any error, return a 401 Unauthorized response
            return JsonResponse({'error': str(e)}, status=401)

        return None
