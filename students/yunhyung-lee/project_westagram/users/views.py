import json
from django.db.models.fields import EmailField

from django.http    import JsonResponse
from django.views   import View

from .models        import User

MINIMUM_PASSWORD_LENGTH = 8

class SignUpView(View):
    def post(self, request):
        data        = json.loads(request.body)
        phone_num   = str(data['phone_num'])
        user_name   = data['user_name']
        password    = data['password']
        email       = data['email']

        if not data['email'] or not data['password']:
            return JsonResponse({'MESSAGE' : '이메일, 패스워드가 공백입니다.'}, status=400)

        elif len(password) < MINIMUM_PASSWORD_LENGTH:
            return JsonResponse({'MESSAGE' : '패스워드가 짧습니다'}, status=400)

        elif User.objects.filter(email=email, user_name=user_name, phone_num=phone_num):
            return JsonResponse({'MESSAGE' : '현재 사용중입니다.'}, status=400)
        
        elif ('@' or '.') not in data['email']:
            return JsonResponse({'MESSAGE' : '형식에 맞지 않습니다.'}, status=400)

        elif not phone_num.isdigit():
            return JsonResponse({'MESSAGE' : '숫자를 입력해주세요.'}, status=400)

        User.objects.create(
                user_name   = user_name,
                phone_num   = phone_num,
                password    = password,
                email       = email
                )
        
        return JsonResponse({'MESSAGE' : 'SUCCESS!'}, status=201)
