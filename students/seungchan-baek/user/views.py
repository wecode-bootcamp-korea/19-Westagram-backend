import json
import re
import bcrypt

from django.views import View
from django.http  import JsonResponse

from user.models  import User

class SignUpView(View):
    def post(self, request):
        data                 = json.loads(request.body)
        email_check          = re.compile('[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        phone_number_check   = re.compile('^\d{3}-\d{3,4}-\d{4}$')
        password_check       = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')

        try:
            password       = data['password']
            name           = data['name']
            nickname       = data['nickname']

            if 'email' in data:
                if User.objects.filter(email=data['email']):
                    return JsonResponse({'MESSAGE':'EMAIL_ALREADY_EXIST'}, status=400)
                elif not email_check.match(data['email']):
                    return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)

            else:
                if User.objects.filter(phone_number=data['phone_number']):
                    return JsonResponse({'MESSAGE':'PHONE_NUMBER_ALREADY_EXIST'}, status=400)
                elif not phone_number_check.match(data['phone_number']):
                    return JsonResponse({'MESSAGE':'INVALID_PHONE_NUMBER'}, status=400)

            if User.objects.filter(nickname=nickname):
                return JsonResponse({'MESSAGE':'NICKNAME_ALREADY_EXIST'}, status=400)

            if not password_check.match(password):
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=400)

            else:
                if 'email' in data:
                    User.objects.create(
                        email          = data['email'],
                        password       = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
                        name           = name,
                        nickname       = nickname
                    )
                    return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

                if 'phone_number' in data:
                    User.objects.create(
                        phone_number   = data['phone_number'],
                        password       = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
                        name           = name,
                        nickname       = nickname
                    )
                    return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)


        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)



class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if 'identification' in data:
                if not User.objects.filter(identification=data['identification']) or not User.objects.filter(password=data['password']):
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
                else:
                    return JsonResponse({"message": "SUCCESS"}, status=200)

            if 'nickname' in data:
                if not User.objects.filter(nickname=data['nickname']) or not User.objects.filter(password=data['password']):
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
                else:
                    return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)






