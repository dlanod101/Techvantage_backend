from django.db import models
from authapp.models import FirebaseUser

def get_default_user():
    user, created = FirebaseUser.objects.get_or_create(
        uid='Default_uid', 
        defaults={'email': 'default@example.com', 'display_name': 'Default User'}
    )
    return user.id  # Return the ID of the user


# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE, related_name='event', default=get_default_user)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='event/user_upload')
    link = models.URLField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title