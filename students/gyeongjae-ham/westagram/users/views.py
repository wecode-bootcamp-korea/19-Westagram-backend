import json

from django.http     import JsonResponse
from django.views    import View

from .models import User
from .validation import validator_email, validator_number, validator_password

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE':'DUPLICATED_EMAIL'}, status=400)

            if User.objects.filter(name=data['name']).exists():
                return JsonResponse({'MESSAGE':'DUPLICATED_NAME'}, status=400)

            if User.objects.filter(number=data['number']).exists():
                return JsonResponse({'MESSAGE':'DUPLICATED_NUMBER'}, status=400)

            if not validator_email(data['email']):
                return JsonResponse({'MESSAGE':'INVALIED_EMAIL'}, status=400)

            if not validator_password(data['password']):
                return JsonResponse({'MESSAGE':'INVALIED_PASSWORD'}, status=400)

            if not validator_number(data['number']):
                return JsonResponse({'MESSAGE':'INVALIED_NUMBER'}, status=400)

            User.objects.create(
            name     = data['name'],
            email    = data['email'],
            phone    = data['phone'],
            password = data['password']
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists() == False:
                return JsonResponse({'MESSAGE':'INVALIED_USER'}, status=401)

            if User.objects.filter(password=data['password']).exists() == False:
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

            if User.objects.filter(email=data['email']).exists():
                User.objects.get(email=data['email'])

                if User.objects.filter(password=data['password']).exists():
                    return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except:
            return JsonResponse( {'MESSAGE': "KEY_ERROR"}, status=400)
