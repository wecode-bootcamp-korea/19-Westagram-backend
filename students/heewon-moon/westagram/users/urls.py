from django.urls import path

from .views      import SignUpView, SignInView, FollowView

urlpatterns = [
    path('/sign_up', SignUpView.as_view()),
    path('/sign_in', SignInView.as_view()),
    path('/follow', FollowView.as_view())
]