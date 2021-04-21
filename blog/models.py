from django.db import models
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy, reverse
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.TextField(max_length=128)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField('auth.User', related_name="post_likes")

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk':self.id})

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comment_fk', on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=128)
    create_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        comment = get_object_or_404(Comment, id=self.pk)
        return reverse('detail', kwargs={'pk':comment.post.id})

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-create_date"]
