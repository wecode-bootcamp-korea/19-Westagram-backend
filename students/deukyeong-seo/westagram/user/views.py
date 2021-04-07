import json, bcrypt, jwt, re

from django.views import View
from django.http  import JsonResponse

import my_settings
from .models import User


class SignUp(View):
    
    def post(self, request):
        
        data                    = json.loads(request.body)
        MINIMUM_PASSWORD_LENGTH = 8
        
        try:

            email_check     = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            email_check     = email_check.match(data['email'])
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            if email_check == None:
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)

            if len(data['password']) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'DUPLICATE_EMAIL'}, status=400)

            User.objects.create(
                    name     = data['name'],
                    email    = data['email'],
                    password = hashed_password.decode('utf-8')
                    )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class LogIn(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(email=data['email']).exists():

                user           = User.objects.get(email=data['email'])
                input_password = data['password'].encode('utf-8')

                if bcrypt.checkpw(input_password, user.password.encode('utf-8')):
                    token = jwt.encode({'user_id':user.id}, my_settings.JWT_SECRET, algorithm=my_settings.JWT_ALGORITHM)
                    return JsonResponse(
                            {
                                'message':'SUCCESS',
                                'token':token
                                },
                            status=200)
                
                else:
                    return JsonResponse({'message':'INCORRECT_PASSWORD'}, status=401)

            else:
                return JsonResponse({'message':'INCORRECT_EMAIL'}, status=401)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
