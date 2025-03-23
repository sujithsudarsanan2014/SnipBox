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
        fields = ['title',]

# Snippet list serializer with links
class SnippetSerializerListWithLinks(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    def get_detail_url(self, obj):
        return settings.BASE_URL+'api/snippet/detail/'+str(obj.id)+'/'

    def get_created_by(self, obj):
        return obj.created_by.username

    class Meta:
        model = Snippet
        fields = ['id', 'title','detail_url','created_by']

# Snippet list serializer
class SnippetSerializer(serializers.ModelSerializer):
    tag = serializers.ListField(child=serializers.CharField(max_length=100))
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'note', 'created_at', 'updated_at', 'tag']

    def list(self, validated_data):
        tags_data = validated_data.pop('tag', [])
        snippet = Snippet.objects.create(**validated_data)

        tag_objects = []
        for tag_data in tags_data:
            tag = Tag.objects.filter(title=tag_data).first()
            if not tag:
                tag = Tag.objects.create(title=tag_data)
            tag_objects.append(tag)

        snippet.tag.set(tag_objects)

        return snippet


    def create(self, validated_data):
        tags_data = validated_data.pop('tag', [])
        snippet = Snippet.objects.create(**validated_data)

        tag_objects = []
        for tag_data in tags_data:
            tag = Tag.objects.filter(title=tag_data).first()
            if not tag:
                tag = Tag.objects.create(title=tag_data)
            tag_objects.append(tag)

        snippet.tag.set(tag_objects) 

        return snippet

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tag', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        tag_objects = []
        for tag_data in tags_data:
            tag = Tag.objects.filter(title=tag_data).first()
            if not tag:
                tag = Tag.objects.create(title=tag_data)
            tag_objects.append(tag)
        
        instance.tag.set(tag_objects)
        
        instance.save()
        
        return instance

# Snippet details serializer
class SnippetSerializerDetail(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()

    def get_tag(self, obj):
        tag_urls = [str(tag.title) for tag in obj.tag.all()]
        return tag_urls

    class Meta:
        model = Snippet
        fields = ['id','note','title','tag']