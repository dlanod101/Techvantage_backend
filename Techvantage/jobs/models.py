from django.db import models
from authapp.models import FirebaseUser

def get_default_user():
    user, created = FirebaseUser.objects.get_or_create(
        uid='Default_uid', 
        defaults={'email': 'default@example.com', 'display_name': 'Default User'}
    )
    return user.id  # Return the ID of the user

# Create your models here.
class Job(models.Model):
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE, related_name='job', default=get_default_user)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='job/user_upload')
    job_type = models.CharField(max_length=255, default='general')
    location = models.CharField(max_length=255, default='general')
    experience = models.CharField(max_length=255, default='general')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title