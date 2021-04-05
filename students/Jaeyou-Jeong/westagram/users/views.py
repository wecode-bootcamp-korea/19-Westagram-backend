import json

from django.http import JsonResponse
from django.views import View

from users.models import UserInfo
from users.checks import email_validation

class Sign(View):
    def post(self, request):
        data = json.loads(request.body)
        password_length = 8
        try:
            if len(data['password']) < password_length:
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)
            elif not  email_validation(data['email']):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)
            elif UserInfo.objects.filter(email=data['email']).exists()\
                    or UserInfo.objects.filter(user_name=data['user_name']).exists()\
                    or UserInfo.objects.filter(phone_number=data['phone_number']).exists():
                return JsonResponse({"message": "EXISTS_USER"}, status=400)

            UserInfo.objects.create(
                    email        = data['email'],
                    password     = data['password'],
                    phone_number = data['phone_number'],
                    user_name    = data['user_name']
                    )

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        return JsonResponse({"message": "Success"}, status=201)
