import json
import re

from django.http    import JsonResponse
from django.views   import View

from .models        import Accounts

# 회원가입 뷰
class SignupView(View):

    def post(self, request):
        data     = json.loads(request.body)
        accounts = Accounts.objects.all()
        
        id_validation    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        pw_validation    = re.compile('')
        phone_validation = re.compile('[0-9]')
        
        # ID Validation check. 1st if > 중복 확인, 2nd if > E-mail 형식 확인
        if Accounts.objects.filter(user_id = data['user_id']).exists():
            if not id_validation.match(data['user_id']):
                return JsonResponse({'message': 'KEY_ERROR Invalid ID'}, status = 400)
            return JsonResponse({'message': 'KEY_ERROR ID already exist'}, status = 400)

        # Password Validation check. 1st if > 비밀번호 길이 확인, 2nd if > 비밀번호 복잡도 확인
        if pw_validation.match(data['user_pw']):
            if len(data['user_pw']) < 8:
                return JsonResponse({'message': 'KEY_ERROR Password too short!'}, status = 400)
            return 
        # Phone number Validation check
        # 1st if > 전화번호 길이 확인, 2nd if > 전화번호 형식 확인, 3rd if > 전화번호 중복 확인
        if len(data['user_phone'] > 11) or len(data['user_phone']) < 10:
            if phone_validation.match(int(data['user_phone'])):
                if Accounts.objects.filter(user_phone = data['user_phone']).exists():
                    return JsonResponse({'message': 'KEY_ERROR PHONE number already exist'}, status = 400)
                return JsonResponse({'message': 'KEY_ERROR Wrong PHONE number'}, status = 400)

        Accounts.objects.create(user_id       = data['user_id'],
                                user_pw       = data['user_pw'],
                                user_name     = data["user_name"],
                                user_phone    = data['user_phone'],
                                user_nickname = data['user_nickname'])
            
        return JsonResponse({"message": "Sign up complete!"}, status = 201)

# 로그인 뷰
class LoginView(View):

    def post(self, request):
        data = json.loads(request.body)
        
        
    pass


