import json
import bcrypt

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
                    or User.objects.filter(user_name=data['user_name']).exists()\
                    or User.objects.filter(phone_number=data['phone_number']).exists():
                return JsonResponse({"message": "EXISTS_USER"}, status=400)

            User.objects.create(
                    email        = data['email'],
                    password     = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    phone_number = data['phone_number'],
                    user_name    = data['user_name']
                    )
            return JsonResponse({"message": "Success"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
