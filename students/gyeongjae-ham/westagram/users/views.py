import bcrypt
import json

from django.http     import JsonResponse
from django.views    import View

from .models import User
from .validation import validator_email, validator_phone, validator_password

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE':'DUPLICATED_EMAIL'}, status=400)

            if User.objects.filter(name=data['name']).exists():
                return JsonResponse({'MESSAGE':'DUPLICATED_NAME'}, status=400)

            if User.objects.filter(phone=data['phone']).exists():
                return JsonResponse({'MESSAGE':'DUPLICATED_NUMBER'}, status=400)

            if not validator_email(data['email']):
                return JsonResponse({'MESSAGE':'INVALIED_EMAIL'}, status=400)

            if not validator_password(data['password']):
                return JsonResponse({'MESSAGE':'INVALIED_PASSWORD'}, status=400)

            if not validator_phone(data['phone']):
                return JsonResponse({'MESSAGE':'INVALIED_NUMBER'}, status=400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
            name     = data['name'],
            email    = data['email'],
            phone    = data['phone'],
            password = hashed_password
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if data['account']:
                if User.objects.filter(email=data['account']).exists():
                    valid_password = User.objects.get(email=data['account']).password.encode('utf-8')

                elif User.objects.filter(phone=data['account']).exists():
                    valid_password = User.objects.get(phone=data['account']).password.encode('utf-8')

                else:
                    return JsonResponse({'MESSAGE':'INVALIED_USER'}, status=400)

            else:
                return JsonResponse({'MESSAGE':'VALUE_EMPTY'}, status=400)

            if bcrypt.checkpw(data['password'].encode('utf-8'), valid_password):
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

            else:
                return JsonResponse({'MESSAGE':'INVALIED_PASSWORD'}, status=400)

        except KeyError:
            return JsonResponse( {'MESSAGE': "KEY_ERROR"}, status=400)
