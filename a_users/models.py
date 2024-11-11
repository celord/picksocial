from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    realname = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar_default.svg')
        return avatar

    @property
    def name(self):
        if self.realname:
            name = self.realname
        else:
            name = self.user.username
        return name