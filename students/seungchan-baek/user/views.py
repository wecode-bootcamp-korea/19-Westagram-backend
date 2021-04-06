import json
import re
import bcrypt
import jwt

from django.views       import View
from django.http        import JsonResponse

from user.models        import User
from westagram.settings import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        data               = json.loads(request.body)
        email_check        = re.compile('[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        phone_number_check = re.compile('^\d{3}-\d{3,4}-\d{4}$')
        password_check     = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')

        try:
            email        = data['email']
            phone_number = data['phone_number']
            password     = data['password']
            name         = data['name']
            nickname     = data['nickname']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE':'EMAIL_ALREADY_EXIST'}, status=400)

            if not email_check.match(email):
                return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)

            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'MESSAGE':'PHONE_NUMBER_ALREADY_EXIST'}, status=400)

            if not phone_number_check.match(phone_number):
                return JsonResponse({'MESSAGE':'INVALID_PHONE_NUMBER'}, status=400)

            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'MESSAGE':'NICKNAME_ALREADY_EXIST'}, status=400)

            if not password_check.match(password):
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=400)

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            hashed_password = hashed_password.decode('utf-8')

            User.objects.create(
                email        = data['email'],
                phone_number = data['phone_number'],
                password     = hashed_password,
                name         = name,
                nickname     = nickname
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)



class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)

        password = data['password']

        try:
            if 'email' not in data and 'nickname' not in data and 'phone_number' not in data:
                raise KeyError

            if 'email' in data:
                email = data['email']
                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                else:
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

            if 'nickname' in data:
                nickname=data['nickname']
                if User.objects.filter(nickname=nickname).exists():
                    user = User.objects.get(nickname=nickname)
                else:
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

            if 'phone_number' in data:
                phone_number=data['phone_number']
                if User.objects.filter(phone_number=phone_number).exists():
                    user = User.objects.get(phone_number=phone_number)
                else:
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

            encode_password = user.password.encode('utf-8')
            checked_password = bcrypt.checkpw(password.encode('utf-8'), encode_password)
            if checked_password:
                access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
                return JsonResponse({'TOKEN':access_token}, status=200)
            else:
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)






