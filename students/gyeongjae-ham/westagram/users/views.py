import bcrypt
import json
import jwt

from django.http     import JsonResponse
from django.views    import View

from .models            import User
from .validation        import validator_email, validator_phone, validator_password
from westagram.settings import SECRET_KEY, HS 

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if not validator_email(data['email']):
                return JsonResponse({'MESSAGE':'INVALIED_EMAIL'}, status=400)

            if not validator_password(data['password']):
                return JsonResponse({'MESSAGE':'INVALIED_PASSWORD'}, status=400)

            if not validator_phone(data['phone_number']):
                return JsonResponse({'MESSAGE':'INVALIED_NUMBER'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE':'DUPLICATED_EMAIL'}, status=400)

            if User.objects.filter(name=data['name']).exists():
                return JsonResponse({'MESSAGE':'DUPLICATED_NAME'}, status=400)

            if User.objects.filter(phone_number=data['phone_number']).exists():
                return JsonResponse({'MESSAGE':'DUPLICATED_NUMBER'}, status=400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
            name         = data['name'],
            email        = data['email'],
            phone_number = data['phone_number'],
            password     = hashed_password
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['account']).exists():
                user = User.objects.get(email=data['account'])

            elif User.objects.filter(phone_number=data['account']).exists():
                user = User.objects.get(phone_number=data['account'])

            else:
                return JsonResponse({'MESSAGE':'INVALIED_USER'}, status=400)

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm=HS)
                return JsonResponse({'MESSAGE':'SUCCESS', 'Token':token}, status=200)
            return JsonResponse({'MESSAGE':'INVALIED_PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse( {'MESSAGE': "KEY_ERROR"}, status=400)
