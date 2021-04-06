import bcrypt
import json
import re

from django.views import View
from django.http  import JsonResponse

from .models      import User

class SignUpView(View):
    def post(self, request):
        data         = json.loads(request.body)
        name         = data['name']
        email        = data['email']
        phone_number = str(data['phone_number'])

        check_email     = re.compile('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')
        valid_email     = re.search(check_email, email)
        check_password  = re.compile('^(?=.*[A-Z])(?=.*\d)(?=.*[a-z])(?=.*[!@#$%&*])(\S){8,}$')
        valid_password  = re.search(check_password, data['password'])
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        password        = hashed_password.decode('utf-8')
        
        try:
            
            if 'email' not in data or 'password' not in data:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)
            
            if not valid_email:
                return JsonResponse({'message': 'VALID_EMAIL'}, status=400)
                
            if not valid_password:
                return JsonResponse({'message': 'VALID_PASSWORD'}, status=400)
                
            if User.objects.filter(email=email):
                return JsonResponse({'message': 'DUPLICATE_EMAIL'}, status=400)
                
            if User.objects.filter(name=name):
                return JsonResponse({'message': 'DUPLICATE_NAME'})
    
            if not phone_number.isdigit():
                return JsonResponse({'message': 'INVALID_PHONE_NUMBER'}, status=400)
                    
            if User.objects.filter(phone_number=phone_number): 
                return JsonResponse({'message': 'DUPLICATE_PHONE_NUMBER'}, status=400)
                
            User.objects.create(
                    name         = name,
                    email        = email,
                    password     = password,
                    phone_number = phone_number 
                )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'meaasege': 'KEY_ERROR'}, status=400)
        
class LoginView(View):
    def post(self, request):

        try:
            
            data = json.loads(request.body)
            password=data['password']

            if user := User.objects.filter(name=data['account']):
                
                if bcrypt.checkpw(password.encode('utf-8'),user.get().password.encode('utf-8')):
                    return JsonResponse({'message': 'SUCCESS'}, status=200)

                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            
            if user := User.objects.filter(email=data['account']):

                if bcrypt.checkpw(password.encode('utf-8'), user.get().password.encode('utf-8')):
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
                
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
                    
            if user := User.objects.filter(phone_number=data['account']):
    
                if bcrypt.checkpw(password.encode('utf-8'), user.get().password.encode('utf-8')):
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
                
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
