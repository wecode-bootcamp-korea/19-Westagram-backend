import json
import bcrypt
import jwt
import re

from django.http    import JsonResponse
from django.views   import View

from .models        import Accounts

# 회원가입 뷰
class SignupView(View):

    def post(self, request):
        data     = json.loads(request.body)
        
        email_validation    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
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
                return JsonResponse({'message': 'Invalid User'}, status = 400)
            
            if not password_validation.search(data['password']):
                return JsonResponse({'message': 'Invalid User'}, status = 400)
            
            if name_validation.search(data['name']):
                return JsonResponse({'message': "Invalid User"}, status = 400)
            
            if len(data['phone']) > MAX_PHONE or len(data['phone']) < MIN_PHONE or not phone_validation.match(data['phone']):
                return JsonResponse({'message': "Invalid User"}, status = 400)
            
            if Accounts.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': "Already exist email"}, status = 400)
            
            if Accounts.objects.filter(nickname = data['nickname']).exists():
                return JsonResponse({'message': 'Already exist nickname'}, status = 400)
            
            if Accounts.objects.filter(phone = data['phone']).exists():
                return JsonResponse({'message': "Already exist phone"}, status = 400)
            
            encrypted_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            Accounts.objects.create(email    = data['email'],
                                    password = encrypted_password,
                                    name     = data['name'],
                                    nickname = data['nickname'],
                                    phone    = data['phone'],)
            
            return JsonResponse({"message": "Sign up complete!"}, status = 201)
        
        except KeyError as error_source:
            return JsonResponse({'message': "KEY ERROR!"}, status = 400)
        
# 로그인 뷰
class LoginView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        pass
        # try:
            
            # if request_id := data.get('email'):
            #     if bcrypt.checkpw(data['password'].encode("utf-8"), Accounts.objects.get(email = request_id).password.encode('utf-8')):
            #         return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
            #     else:
            #         return JsonResponse({'message': 'Invalid user'}, status = 401)
                
            # if request_id := data.get('nickname'):
            #     if bcrypt.checkpw(data['password'].encode("utf-8"), Accounts.objects.get(nickname = request_id).password.encode('utf-8')):
            #         return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
            #     else:
            #         return JsonResponse({'message': 'Invalid user'}, status = 401)
                
            # if request_id := data.get('phone'):
            #     if bcrypt.checkpw(data['password'].encode("utf-8"), Accounts.objects.get(phone = request_id).password.encode('utf-8')):
            #         return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
            #     else:
            #         return JsonResponse({'message': 'Invalid user'}, status = 401)
            
            # if accounts.filter(email = data["account"]).exists():
            #     request_id = accounts.get(email = data.get('account'))
            
            # if accounts.filter(nickname = data['account']).exists():
            #     request_id = accounts.get(nickname = data.get('account'))
            
            # if accounts.filter(phone = data['account']).exists():
            #     request_id = accounts.get(phone = data.get('account'))
                
            # if bcrypt.checkpw(data['password'].encode("utf-8"), request_id.password.encode('utf-8')):
            #     return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
            # else:
            #     return JsonResponse({'message': 'Invalid user'}, status = 401)
            
        # except KeyError as error_source:
        #     return JsonResponse({'message': f"KEY ERROR, {error_source} is WRONG"}, status = 400)
        
        # except Accounts.DoesNotExist as error_source:
        #     return JsonResponse({'message': f"{error_source} is Invalid ID"}, status = 400)