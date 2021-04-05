import json

from django.http     import JsonResponse
from django.views    import View

from .models import User

class CreateUserView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists() == True:
                return JsonResponse({'MESSAGE':'이미 등록된 이메일입니다.'}, status=400)
            elif User.objects.filter(name=data['name']).exists() ==  True:
                return JsonResponse({'MESSAGE':'이미 등록된 사용자입니다.'}, status=400)
            elif User.objects.filter(number=data['number']).exists() == True:
                return JsonResponse({'MESSAGE':'이미 등록된 번호입니다.'}, status=400)
            elif not '@' in data['email'] or not '.' in data['email']:
                return JsonResponse({'MESSAGE':'유효한 이메일 형식이 아닙니다.'}, status=400)
            elif len(data['password']) < 8:
                return JsonResponse({'MESSAGE':'비밀번호는 8자리 이상입니다.'}, status=400)

            User.objects.create(
            name = data['name'],
            email = data['email'],
            number = data['number'],
            password = data['password']
            )

        except KeyError:

            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

class LoginView(View):
    def get(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists() == False:
                return JsonResponse({'MESSAGE':'INVALIED_USER'}, status=401)
            elif User.objects.filter(password=data['password']).exists() == False:
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
            elif User.objects.filter(email=data['email']).exists() == True:
                User.objects.get(email=data['email'])
                if User.objects.filter(password=data['password']).exists() == True:
                    return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except:
            return JsonResponse( {'MESSAGE': "KEY_ERROR"}, status=400)
