from django.urls import path
from .views import UserView, SignInView

urlpatterns = [
    path('/users', UserView.as_view()),
    path('/login', SignInView.as_view())
]

# path('/users', UserView.as_view())

# 8000:users 이게 큰 url /users 이렇게, 이런거는 다 정하는 것!!!

# 없는 키를 보냈을 때, 어떻게 되나? 그냥 들어옴 키를 설정해 놓고, 가야함??

