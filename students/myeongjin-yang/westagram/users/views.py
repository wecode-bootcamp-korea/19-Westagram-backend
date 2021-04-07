import json
import re
import bcrypt
import jwt
import my_settings

from django.http  import JsonResponse
from django.views import View 

from users.models import User

class SignUpView(View):
    def post(self,request):
        data               = json.loads(request.body)
        email_check        = re.compile('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')
        phonenumber_check  = re.compile('[0-9]{3}[0-9]{4}[0-9]{4}')
        PASSWORD_CHECK     = 8

        try:
            email          = data['email']
            phonenumber    = data['phonenumber']
            password       = data['password']
            name           = data['name']
            username       = data['username']

            if not email_check.match(email) or not phonenumber_check.match(phonenumber):
                return JsonResponse({'message':"Invalid ID"}, status=400)

            if len(password) < PASSWORD_CHECK:
                return JsonResponse({'message':"Invalid PW"}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':"existing ID"}, status=400)

            if User.objects.filter(phonenumber=phonenumber).exists():
                return JsonResponse({'message':"existing phonenumber"}, status=400)

            if User.objects.filter(username = username):
                return JsonResponse({'message':"existing username"}, status=400)


            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())       
            
            User.objects.create(
                email       = email, 
                phonenumber = phonenumber,
                password    = hashed_password.decode('utf-8'), 
                name        = name, 
                username    = username
                )
            
            return JsonResponse({'message':"SUCCESS"}, status=200)
        
        except KeyError:
            return JsonResponse({'message':"KEY_ERROR"}, status=400)
        
class SignInView(View):
    def post(self,request):
        data               = json.loads(request.body)
        try:
            if 'email' in data:
                email       = data['email']
                password    = data['password']

                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                else:
                    return JsonResponse({'message':"INVALID_USER"}, status=401)
            
            elif 'username' in data:
                username    = data['username']
                password    = data['password']

                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                else:
                    return JsonResponse({'message':"INVALID_USER"}, status=401)
            
            else:
                phonenumber = data['phonenumber']
                password    = data['password']

                if User.objects.filter(phonenumber=phonenumber).exists():
                    user = User.objects.get(phonenumber=phonenumber)
                else:                   
                    return JsonResponse({'message':"INVALID_USER"}, status=401)
                   

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'username':user.username}, my_settings.SECRET, algorithm='HS256')
                return JsonResponse({'access_token':access_token}, status=200)
            
            else:               
                return JsonResponse({'message':"WRONG_PASSWORD"}, status=401)

        except KeyError:
            return JsonResponse({'message':"KEY_ERROR"}, status=400)