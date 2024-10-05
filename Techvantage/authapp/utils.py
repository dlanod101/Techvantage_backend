# your_app/utils.py
from .models import FirebaseUser

def get_or_create_firebase_user(uid):
    """
    Retrieve or create a FirebaseUser based on the given UID.
    """
    try:
        # Get or create the user in the database
        user, created = FirebaseUser.objects.get_or_create(uid=uid)
        return user
    except FirebaseUser.DoesNotExist:
        return None
