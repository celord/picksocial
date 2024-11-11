from django.db import models
from django.contrib.auth.models import User
import uuid


class Post(models.Model):
    title = models.CharField(max_length=500)
    artist = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True)
    image = models.URLField(max_length=500)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='likedposts', through='LikedPost', blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='posts', null=True)
    tags = models.ManyToManyField('Tag', related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, primary_key=True, unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


class LikedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ['user', 'post']

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'


class Tag(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='icons/', null=True, blank=True)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', null=True)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='likedcomments', through='LikedComment')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, primary_key=True, unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        try:
            return f'{self.author.username}: {self.body[:30]}'
        except:
            return f'Anonymous: {self.body[:30]}'

    class Meta:
        ordering = ['-created']


class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ['user', 'post']

    def __str__(self):
        return f'{self.user.username} likes {self.comment.body[:30]}'


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='replies', null=True)
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    likes = models.ManyToManyField(User, related_name='likedreplies', through='LikedReply')
    body = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, primary_key=True, unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        try:
            return f'{self.author.username}: {self.body[:30]}'
        except:
            return f'Anonymous: {self.body[:30]}'

    class Meta:
        ordering = ['-created']


class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ['user', 'post']

    def __str__(self):
        return f'{self.user.username} likes {self.reply.body[:30]}'
