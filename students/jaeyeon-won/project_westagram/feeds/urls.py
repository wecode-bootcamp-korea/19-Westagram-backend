from django.urls import path
from .views import FeedView,PostView
urlpatterns = [
    path('',FeedView.as_view())
]