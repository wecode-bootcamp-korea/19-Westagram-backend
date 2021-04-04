import json

from django.http import JsonResponse
from django.views import View

from users.models import Signin

class Sign(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            find_1 = data['email'].find('@')
            find_2 = data['email'].find('.')
            if len(data['password']) < 8:
                return JsonResponse({"message": "비밀번호는 8자리 이상으로 만들어 주세요."}, status=400)
            elif find_1 == -1\
                    or find_2 == -1\
                    or find_1 > find_2\
                    or find_2 == len(data['email']) - 1:
                return JsonResponse({"message": "이메일 양식에 맞춰주세요."}, status=400)
            elif Signin.objects.filter(email=data['email']).exists()\
                    or Signin.objects.filter(user_name=data['user_name']).exists()\
                    or Signin.objects.filter(phone_number=data['phone_number']).exists():
                return JsonResponse({"message": "이미 존재하는 사용자 입니다."}, status=400)

            Signin.objects.create(
                    email        = data['email'],
                    password     = data['password'],
                    phone_number = data['phone_number'],
                    user_name    = data['user_name']
                    )

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        return JsonResponse({"message": "Success"}, status=201)
