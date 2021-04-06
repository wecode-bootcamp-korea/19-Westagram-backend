import json
from django.http import JsonResponse
from django.views import View
from users.models import User


# Create your views here.

class SignUpView(View):
    def post(self, request):
        # data = json.loads(request.body)
        user_db = User.objects.all()
        PASSWORD_LENGTH = 8  # 편의상 상수처리.

        try:
            data = json.loads(request.body)

            if not "@" in data['email'] or not "." in data['email']:
                return JsonResponse({'message': 'use valid email'}, status=400)

            if user_db.filter(email=data['email']).exists():
                return JsonResponse({'message': 'This email already exists!'}, status=400)

            if not data['email'] or not data['password']:
                return JsonResponse({'message': 'email & password are required'}, status=400)

            if len(data['password']) < PASSWORD_LENGTH:
                return JsonResponse({'message': 'use stronger password'}, status=400)

            User.objects.create(
                email=data['email'],
                password=data['password'],
                phone_number=data['phone_number']
            )
            return JsonResponse({'message': 'SUCCESS'}, status=200)


        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)
