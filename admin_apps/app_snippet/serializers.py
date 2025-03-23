# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from .models import *

# User serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

# Tag serializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']

class SnippetSerializerListWithLinks(serializers.ModelSerializer):
    tag = TagSerializer(many=True)   
    detail_url = serializers.SerializerMethodField()

    def get_detail_url(self, obj):
        return settings.BASE_URL+'api/snippet/detail/'+str(obj.id)+'/'

    class Meta:
        model = Snippet
        fields = ['id', 'title','tag','detail_url']

# Snippet serializer
class SnippetSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)   

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'note', 'created_at', 'updated_at', 'tag']

    def create(self, validated_data):
        tags_data = validated_data.pop('tag', [])
        snippet = Snippet.objects.create(**validated_data)
        for tag_data in tags_data:
            tag = Tag.objects.get_or_create(title=tag_data['title'])
            snippet.tags.add(tag)
        
        return snippet

    # def update(self, instance, validated_data):
    #     tags_data = validated_data.pop('tags', [])
        
    #     # Update Snippet fields
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.note = validated_data.get('note', instance.note)
    #     instance.save()

    #     # Update tags
    #     instance.tags.clear()  # Clear old tags
    #     for tag_data in tags_data:
    #         tag, created = Tag.objects.get_or_create(title=tag_data['title'])
    #         instance.tags.add(tag)

    #     return instance
