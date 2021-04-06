import json, re
from .models            import User
from django.db.models   import aggregates
from django.http        import JsonResponse
from django.views       import View

class UserView(View):
    def post(self, request):
        data        = json.loads(request.body)
        login_id    = data['email']
        login_pw    = data['password']
        nickname    = data['nickname']
        name        = data['name']
        phone       = data['phone']
        pw_length   = 8
        phone_check = re.compile('^[0-9]{3}[0-9]{3,4}[0-9]{4}')
        email_check = re.compile('^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$')


        if len(login_id) <= 0 or len(login_pw) == 0 :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        if len(name) == 0 or len(nickname) == 0:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        if not email_check.match(login_id):
            return JsonResponse({'message':'Invaild ID_ERROR'}, status=400)
        
        if not phone_check.match(phone):
            return JsonResponse({'message':'Invaild PHONE_ERROR'}, status=400)
           
        if len(login_pw) < pw_length:
            return JsonResponse({'message':'Invaild PW_ERROR'}, status=400)

        if User.objects.filter(nickname = nickname):
            return JsonResponse({'message':'Nickname Duplicate_ERROR'}, status=400)
        
        if User.objects.filter(email = login_id):
            return JsonResponse({'message':'ID Duplicate_ERROR'}, status=400)
        
        if User.objects.filter(phone = phone):
            return JsonResponse({'message':'Phone Duplicate_ERROR'}, status=400)

        User.objects.create(
                    email    = data['email'],
                    password = data['password'],
                    nickname = data['nickname'],
                    name     = data['name'],
                    phone    = data['phone'])
        return JsonResponse({'message':'SUCCESS'}, status=200)


class LoginView(View):
    def post(self,request):
        data        = json.loads(request.body)
        login_id    = data['id']
        login_pw    = data['password']
        phone_check = re.compile('^[0-9]{3}[0-9]{3,4}[0-9]{4}')
        email_check = re.compile('^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$')


        if login_id == "" or login_pw == "" :
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        if phone_check.match(login_id):
            if not User.objects.filter(phone=login_id) or not User.objects.filter(password=login_pw):
                return JsonResponse({'message':'INVALID_USER'}, status = 401)

        if email_check.match(login_id):
            if not User.objects.filter(email=login_id) or not User.objects.filter(password=login_id):
                return JsonResponse({'message':'INVALID_USER'}, status = 401)
        
        if not email_check.match(login_id) and not phone_check.match(login_id):
            if not User.objects.filter(nickname=login_id) or not User.objects.filter(password=login_pw):
                return JsonResponse({'message':'INVALID_USER'}, status = 401)

        return JsonResponse({'message':'SUCCESS'}, status = 200)
