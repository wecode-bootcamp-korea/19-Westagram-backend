import json

from django.views import View
from django.http import JsonResponse

from .models import User

class SignupView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            name = data['name']
            phone_number = data['phone_number']
            email = data['email']
            username = data ['username']
            password = data['password']

            if name =='':
                return JsonResponse({'message' : '이름을 입력하세요!'}, status = 400)
            if phone_number =='' and email =='':
                return JsonResponse({'message' : '휴대폰 번호 혹은 이메일을 입력해주세요!'},status = 400)
            if username =='':
                return JsonResponse({'message' : 'username을 입력하세요!'}, status = 400)
            if password == '':
                return JsonResponse({'message' : '비밀번호를 입력하세요!'}, status = 400)
            if '@' not in email or '.' not in email:
                return JsonResponse({'messsage' : '이메일 형식에 맞게 작성해주세요!'}, status = 400)
            #if not phone_number[:2] == 10 or phone_number[:2] == 11 or phone_number[:2] == 16 or phone_number[:2] == 17 or phone_number[:2] == 19:
            #    return JsonResponse({'형식에 맞는 휴대폰번호를 입력해주세요!'}, status = 400)
            if len(password) <= 7:
                return JsonResponse({'message' : '비밀번호는 8자리 이상으로 작성해주세요'}, status = 400)
            if User.objects.filter(phone_number = phone_number):
                return JsonResponse({'message' : '이미 존재하는 휴대폰 번호입니다.'}, status = 400)
            if User.objects.filter(username = username):
                return JsonResponse({'message' : '이미 존재하는 username입니다.'}, status = 400)
            if User.objects.filter(email = email):
                return JsonResponse({'message' : '이미 가입되어 있는 이메일 입니다.'}, status = 400)

            User.objects.create(
                name = name,
                phone_number=phone_number,
                email=email,
                username=username,
                password=password
                )
            return JsonResponse({'message' : '회원가입을 축하합니다!'}, status = 200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
'''
    class SigninView(View):
        def post(self,request):
            data = json.loads(request.body)
            try:
                email = data['email']
                password = data['password']
                if User.objects.filter(email=email).exists():           # filter().exists()는 T or F 출력
                    if password =='':
                        return JsonResponse({'message': '비밀번호를 입력해주세요!'},status = 400)
                    if User.objects.filter(password=password).exists():
                        return JsonResponse({'message': '로그인에 성공했습니다!'}, status = 200)
                    else:
                        return JsonResponse({'message': '비밀번호를 확인해주세요'}, status = 400)
'''
            
        

            
            
    






        