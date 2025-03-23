from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class Snippet(models.Model):
    title = models.CharField(max_length=255)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets')
    tag = models.ManyToManyField(Tag, related_name='snippets', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']