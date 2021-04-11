from django.urls import path

from .views      import FeedView, IndexView, DetailView, CommentView, LikeView

urlpatterns = [
    path('/create', FeedView.as_view()),
    path('/feed/<int:feed_id>', DetailView.as_view()),
    path('/comments/<int:feed_id>/add', CommentView.as_view()),
    path('/like/<str:content>/<int:content_id>', LikeView.as_view()),
    path('', IndexView.as_view())
]