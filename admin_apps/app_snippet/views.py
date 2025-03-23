# views.py
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *

def generate_api_response(success, data, message):
    return {"success": success, "message": message, "data": data, }

class CreateUserAPI(APIView):
    """
    API for creating a new user.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OverviewAPI(APIView):
    """
    API for getting the total number of snippets and list all available snippets with a hyperlink to respective detail APIs.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            total_snippets = Snippet.objects.filter(created_by=request.user).count()
            snippets = Snippet.objects.filter(created_by=request.user)
            snippet_serializer = SnippetSerializerListWithLinks(snippets, many=True)
            if snippets:
                serializer = SnippetSerializerListWithLinks(snippets, many=True)
                data = {
                "total_count": total_snippets,
                "snippets": snippet_serializer.data
                }
                response_data=generate_api_response(True, data, "successfully retrieved snippet list with links")
            else:
                response_data = generate_api_response(False, [], "No data found")
            return Response(response_data, status=200)

        except Snippet.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        

class DetailSnippetAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SnippetSerializer

    def get(self, request, snippet_id):
        try:
            snippet = Snippet.objects.filter(id=snippet_id, created_by=request.user)
            if snippet:
                serializer = SnippetSerializer(snippet, many=True)
                response_data=generate_api_response(True, serializer.data, "successfully retrieved snippet details")
            else:
                response_data = generate_api_response(False, [], "No data found")
            return Response(response_data, status=200)
        except Snippet.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
class TagListAPI(viewsets.ModelViewSet):
    """
    API view to list tags
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        try:
            tags = Tag.objects.all()
            serializer = self.get_serializer(tags,many=True, context={"request": request})
            if serializer.data:
                response_data = generate_api_response(True, serializer.data, "successfully retrieved tags list")
            else:
                response_data = generate_api_response(
                    False, [], "No data found")
            return Response(response_data, status=200)
        except Exception as error:
            response_data = generate_api_response(
                False, [], f"An error occurred: {str(error)}")
            return Response(response_data, status=500)


class SnippetCreateAPIView(APIView):
    """
    API view to create a new snippet with tags.
    """
    permission_classes = [IsAuthenticated] 
    serializer_class = SnippetSerializer

    def post(self, request):
        serializer = SnippetSerializer(data=request.data)
        print("on post")
        if serializer.is_valid():
            # Add the current user to the validated data
            validated_data = serializer.validated_data
            validated_data['created_by'] = request.user
            
            # Create the Snippet
            snippet = serializer.create(validated_data)

            return Response({
                'message': 'Snippet created successfully.',
                'snippet': {
                    'title': snippet.title,
                    'note': snippet.note,
                    'created_at': snippet.created_at,
                    'updated_at': snippet.updated_at,
                    'tag':[tag.title for tag in snippet.tag.all()]
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteSnippetAPI(APIView):
    """
    API view to delete a selected snippet and return rest of the snippets
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            snippet_id=request.data.get("snippet_id","")
            snippet = Snippet.objects.get(id=snippet_id, created_by=request.user)
            if snippet:
                snippet.delete()
                # Return the updated list of snippets
                remaining_snippets = Snippet.objects.filter(created_by=request.user)
                serializer = SnippetSerializer(remaining_snippets, many=True)
                response_data = generate_api_response(True, serializer.data, "Given snippet deleted")
                return Response(response_data, status=200)
        except Exception as error:
            response_data = generate_api_response(
                False, [], f"An error occurred: {str(error)}")
            return Response(response_data, status=500)

class UpdateSnippetAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, snippet_id):
        try:
            snippet = Snippet.objects.get(id=snippet_id, created_by=request.user)
            if snippet:
                serializer = SnippetSerializer(snippet, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                response_data = generate_api_response(True, serializer.data, "Given snippet data updated")
                return Response(response_data, status=200)
            else:
                response_data = generate_api_response(False, [], "No data found")
        except Exception as error:
            response_data = generate_api_response(
                False, [], f"An error occurred: {str(error)}")
