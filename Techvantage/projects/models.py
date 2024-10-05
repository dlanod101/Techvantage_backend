from django.db import models
from authapp.models import FirebaseUser

def get_default_user():
    user, created = FirebaseUser.objects.get_or_create(
        uid='Default_uid', 
        defaults={'email': 'default@example.com', 'display_name': 'Default User'}
    )
    return user.id  # Return the ID of the user

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE, related_name='project', default=get_default_user)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='project/user_upload')
    category = models.CharField(max_length=100)
    contributors = models.CharField(max_length=200)
    published_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)  # Must be defined


    def __str__(self):
        return self.title