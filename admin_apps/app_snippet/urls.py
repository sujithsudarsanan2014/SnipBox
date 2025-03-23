from django.urls import path, include
from .views import *

urlpatterns = [
    path('auth/register/', CreateUserAPI.as_view(), name='user-create-api'),
    path('overview/', OverviewAPI.as_view(), name='overview-api'),
    path('create/', SnippetCreateAPIView.as_view(), name='create-snippet-api'),
    path('tags/', TagListAPI.as_view({'get': 'list'}), name='list-tags-api')
]
