from django.urls     import path
from .views import PostingView, DisplayView

urlpatterns = [
    path('/posting', PostingView.as_view()),
    path('/display', DisplayView.as_viwe()),
    ]