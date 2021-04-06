import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View
from users.models import User

class SignUpView(View):
    def post(self,request):

        PASSWORD_LENGTH = 8

        try:
            data = json.loads(request.body)

            if not "@" in data['email'] or not "." in data['email']:
                return JsonResponse({'message': 'USE_VALID_EMAIL'}, status=400)

            if User.objects.filter(email=data['email']).exists() or \
                    User.objects.filter(nickname=data['nickname']).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400)

            if not data['email'] or not data['password'] or not data['nickname']:
                return JsonResponse({'message': 'FILL_IN_EVERYTHING'}, status=400)

            if len(data['password']) < PASSWORD_LENGTH:
                return JsonResponse({'message': 'SHORT_PASSWORD'}, status=400)

            hashed_password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                email        = data['email'],
                password     = hashed_password,
                phone_number = data['phone_number'],
                name         = data['name'],
                nickname     = data['nickname'],
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LogInView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:


           if User.objects.filter(email=data['email']).exists() and \
                    User.objects.filter(password=data['password']).exists():
                return JsonResponse({'message': 'LOGIN_SUCCESS'}, status=201)

           if User.objects.filter(nickname=data['nickname']).exists() and \
                   User.objects.filter(password=data['password']).exists():
               return JsonResponse({'message': 'LOGIN_SUCCESS'}, status=201)

           if User.objects.filter(phone_number=data['phone_number']).exists() and \
                   User.objects.filter(password=data['password']).exists():
               return JsonResponse({'message': 'LOGIN_SUCCESS'}, status=201)

           else:
               return JsonResponse({'message': 'ACCESS_DENIED'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'Key_Error'}, status=400)
