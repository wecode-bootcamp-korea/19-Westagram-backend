import json
import re
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View 

from users.models import User

class SignUpView(View):
    def post(self,request):
        data               = json.loads(request.body)
        email_check        = re.compile('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')
        phonenumber_check  = re.compile('[0-9]{3}[0-9]{4}[0-9]{4}')
        password_check     = 8

        try:
            if 'email' in data:
                email       = data['email']
                if not email_check.match(email):
                    return JsonResponse({'message':"Invalid ID"}, status=400)
                if User.objects.filter(email=email).exists():
                    return JsonResponse({'message':"existing ID"}, status=400)

            else:
                phonenumber = data['phonenumber']
                if not phonenumber_check.match(phonenumber):
                    return JsonResponse({'message':"Invalid ID"}, status=400)
                if User.objects.filter(phonenumber=phonenumber).exists():
                    return JsonResponse({'message':"existing ID"}, status=400)

            password        = data['password']
            name            = data['name']
            username        = data['username']
                        
            if len(password)<password_check:
                return JsonResponse({'message':"Invalid PW"}, status=400)

            if User.objects.filter(username = username):
                return JsonResponse({'message':"existing username"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())       
            
            if 'email' in data: 
                User.objects.create(email = email, password = hashed_password.decode('utf-8'), name = name, username = username)
            else:
                User.objects.create(phonenumber = phonenumber, password = hashed_password.decode('utf-8'), name = name, username = username)
            
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

            
        except KeyError:
            return JsonResponse({'message':"KEY_ERROR"}, status=400)
        
        else:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':"SUCCESS"}, status=200)
            
            else:
                return JsonResponse({'message':"INVALID_USER"}, status=401)
        


        
        
