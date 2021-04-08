import json
import bcrypt
import jwt
import re

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from mysetting import ALGORITHM, secret
from .models   import Accounts

# 회원가입 뷰
class SignupView(View):

    def post(self, request):
        data     = json.loads(request.body)
        
        email_validation    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$')
        password_validation = re.compile('[(<`~!@#$%^&*,./?;:>)_]+')
        name_validation     = re.compile('[ㄱ-ㅎㅏ-ㅣ]+')
        phone_validation    = re.compile('[0-9]+')
        
        MAX_PASSWORD = 30
        MIN_PASSWORD = 8
        MAX_PHONE    = 11
        MIN_PHONE    = 10
        
        try:
            if not email_validation.match(data['email']):
                return JsonResponse({'message': "Invalid User"}, status = 400)

            if len(data['password']) < MIN_PASSWORD or len(data['password']) > MAX_PASSWORD:
                return JsonResponse({'message': 'Password too short!'}, status = 400)
            
            if not re.search('[a-zA-Z]+', data['password']) or not re.search('[0-9]+', data['password']):
                return JsonResponse({'message': 'Password Invalid User'}, status = 400)
            
            if not password_validation.search(data['password']):
                return JsonResponse({'message': 'Pnvalid User'}, status = 400)
            
            if name_validation.search(data['name']):
                return JsonResponse({'message': "Invalid User name"}, status = 400)
            
            if len(data['phone']) > MAX_PHONE or len(data['phone']) < MIN_PHONE or not phone_validation.match(data['phone']):
                return JsonResponse({'message': "Invalid User phone"}, status = 400)
            
            if Accounts.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': "Already exist email"}, status = 400)
            
            # if Accounts.objects.filter(nickname = data['nickname']).exists():
            #     return JsonResponse({'message': 'Already exist nickname'}, status = 400)
            
            if Accounts.objects.filter(phone = data['phone']).exists():
                return JsonResponse({'message': "Already exist phone"}, status = 400)
            
            encrypted_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            Accounts.objects.create(email    = data['email'],
                                    password = encrypted_password,
                                    name     = data['name'],
                                    # nickname = data['nickname'],
                                    phone    = data['phone'],)
            
            return JsonResponse({"message": "Sign up complete!"}, status = 201)
        
        except KeyError:
            return JsonResponse({'message': "KEY ERROR!"}, status = 400)
        
# 로그인 뷰
class LoginView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            request_id = Accounts.objects.filter(Q(email = data['email'])|
                                            # Q(nickname = data.get('account'))|
                                                 Q(phone = data['email'])).first()
            
            if bcrypt.checkpw(data.get('password').encode('utf-8'), request_id.password.encode('utf-8')):
                token = jwt.encode({"user_id": request_id.id}, secret['secret'], ALGORITHM)
                return JsonResponse({'token': token}, status = 200)
            
            return JsonResponse({'message': 'Invalid User'}, status = 400)
            
        except KeyError:
            return JsonResponse({'message': 'Key Error'}, status = 400)
        
        except Exception:
            return JsonResponse({'message': 'Something Wrong'}, status = 404)