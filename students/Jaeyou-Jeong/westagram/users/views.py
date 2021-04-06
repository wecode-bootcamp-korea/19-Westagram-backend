import bcrypt
import json

from django.http import JsonResponse
from django.views import View

from users.models import User
from users.checks import email_validation

class Sign(View):
    def post(self, request):
        data = json.loads(request.body)
        PASSWORD_LENGTH = 8
        try:
            if len(data['password']) < PASSWORD_LENGTH:
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

            if not  email_validation(data['email']):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if User.objects.filter(email=data['email']).exists()\
                    or User.objects.filter(name=data['name']).exists()\
                    or User.objects.filter(phone_number=data['phone_number']).exists():
                return JsonResponse({"message": "EXISTS_USER"}, status=400)

            User.objects.create(
                    email        = data['email'],
                    password     = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    phone_number = data['phone_number'],
                    name    = data['name']
                    )
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class Login(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            if not data['email'] == "":
                Login_User = User.objects.get(email=data['email'])
            elif not data['user_name'] == "":
                Login_User = User.objects.get(name=data['user_name'])
            elif not data['phone_number'] == "":
                Login_User = User.objects.get(phone_number=data['phone_number'])
            else:
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            if data['password'] == "":
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

            if bcrypt.checkpw(data['password'].encode('utf-8'), Login_User.password.encode('utf-8')):
                return JsonResponse({"message": "SUCCESS"}, status=200)
            else:
                return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
