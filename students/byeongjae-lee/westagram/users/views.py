import bcrypt
import json
import jwt
import re

from django.views        import View
from django.http         import JsonResponse
from django.db.models    import Q


from .models      import User

class SignUpView(View):
    def post(self, request):
        data         = json.loads(request.body)
        
        try:
            if 'email' not in data or 'password' not in data:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)
            
            email          = data['email']
            check_email    = re.compile('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')
            valid_email    = re.search(check_email, email)
            check_password = re.compile('^(?=.*[A-Z])(?=.*\d)(?=.*[a-z])(?=.*[!@#$%&*])(\S){8,}$')
            valid_password = re.search(check_password, data['password'])
            
            if not valid_email:
                return JsonResponse({'message': 'VALID_EMAIL'}, status=400)
                
            if not valid_password:
                return JsonResponse({'message': 'VALID_PASSWORD'}, status=400)
            
            if User.objects.filter(
                Q(email        = email)|
                Q(name         = data['name'])|
                Q(phone_number = data['phone_number'])).exists():
                return JsonResponse({'message': 'DUPLICATE_ACCOUNT'}, status=400)
            
            if not data['phone_number'].isdigit():
                return JsonResponse({'message': 'INVALID_PHONE_NUMBER'}, status=400)
                
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            password        = hashed_password.decode('utf-8')
            name            = data['name']
            
            User.objects.create(
                    name         = data['name'],
                    email        = email,
                    password     = password,
                    phone_number = data['phone_number'] 
                )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'meaasege': 'KEY_ERROR'}, status=400)
        
class LoginView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)
            
            password = data['password']

            if user := User.objects.filter(
                Q(name         = data['account'])|
                Q(email        = data['account'])|
                Q(phone_number = data['account'])):
                
                if bcrypt.checkpw(password.encode('utf-8'),user.get().password.encode('utf-8')):
                    return JsonResponse({'message': 'SUCCESS'}, status=200)

            return JsonResponse({'message': 'INVALID_USER'}, status=401)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)