import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View
from users.models import User

class SignUpView(View):
    def post(self,request):

        PASSWORD_LENGTH = 8

        try:
            data = json.loads(request.body)

            if not "@" in data['email'] or not "." in data['email']:
                return JsonResponse({'message': 'USE_VALID_EMAIL'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400)

            if not data['email'] or not data['password'] or not data['nickname']:
                return JsonResponse({'message': 'FILL_IN_EVERYTHING'}, status=400)

            if len(data['password']) < PASSWORD_LENGTH:
                return JsonResponse({'message': 'SHORT_PASSWORD'}, status=400)

            hashed_password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                email        = data['email'],
                password     = hashed_password,
                phone_number = data.get('phone_number',None),
                name         = data.get('name',None),
                nickname     = data.get('nickname',None) ## 단점: 키 에러를 찾기가 힘듦 (디폴트 값이 있기 때문에...)
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LogInView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(email=data['email']).exists():
                user_email = User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user_email.password.encode('utf-8')) ==True:
                   access_token = jwt.encode({'id': user_email.id}, 'secret', algorithm='HS256')
                   return JsonResponse({'token': access_token},status=200)

                else:
                   return JsonResponse({'message':'INCORRECT_PASSWORD'}, status=401)

            else:
                return JsonResponse({'message': 'ID_NOT_EXIST'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)




