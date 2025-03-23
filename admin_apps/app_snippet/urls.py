from django.urls import path, include
from .views import *

urlpatterns = [
    path('auth/register/', CreateUserAPI.as_view(), name='user-create-api'),
    path('overview/', OverviewAPI.as_view(), name='overview-api'),
    path('create/', SnippetCreateAPIView.as_view(), name='create-snippet-api'),
    path('tags/', TagListAPI.as_view({'get': 'list'}), name='list-tags-api'),
    path('delete-snippet/', DeleteSnippetAPI.as_view(), name='delete-snippet-api'),
    path('detail/<int:snippet_id>/', DetailSnippetAPI.as_view(), name='snippet-details-api'),
    path('update/<int:snippet_id>/', UpdateSnippetAPI.as_view(), name='update-snippet-api'),
    path('filter-tags/', FilterByTagAPI.as_view(), name='filter-tags-api'),
]
