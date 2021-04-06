import json
import bcrypt
from django.http import JsonResponse
from django.views import View
from users.models import User


# Create your views here.

class SignUpView(View):
    def post(self, request):

        PASSWORD_LENGTH = 8  # 편의상 상수처리.

        try:
            data = json.loads(request.body)

            if not "@" in data['email'] or not "." in data['email']:
                return JsonResponse({'message': 'USE_VALID_EMAIL'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400)

            if not data['email'] or not data['password'] or not data['nickname']:
                return JsonResponse({'message': 'FILL_IN_EVERYTHING'}, status=400)

            if len(data['password']) < PASSWORD_LENGTH:
                return JsonResponse({'message': 'SHORT_PASSWORD'}, status=400)

            User.objects.create(
                email=data['email'],
                password=data['password'],
                phone_number=data['phone_number'],
                name=data['name'],
                nickname=data['nickname'],
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)


        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class LogInView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists() and \
                    User.objects.filter(password=data['password']).exists():
                return JsonResponse({'message': 'LOG_IN_SUCCESS'}, status=200)
            else:
                return JsonResponse({'message': 'ACCESS_DENIED'})



        except KeyError:
            return JsonResponse({'message': 'Key_Error!'}, status=400)
