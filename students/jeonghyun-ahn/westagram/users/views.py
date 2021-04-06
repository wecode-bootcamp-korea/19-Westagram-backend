import json, re, bcrypt
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
        PW_LENGTH   = 8
        phone_check = re.compile('^[0-9]{3}[0-9]{3,4}[0-9]{4}')
        email_check = re.compile('^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$')


        if len(login_id) <= 0 or len(login_pw) == 0 :
            return JsonResponse({'message':'ID or PW KEY_ERROR'}, status=400)

        if len(name) <= 0 or len(nickname) <= 0:
            return JsonResponse({'message':'NAME or NICKNAME KEY_ERROR'}, status=400)

        if not email_check.match(login_id):
            return JsonResponse({'message':'INVAILD ID_ERROR'}, status=400)
        
        if not phone_check.match(phone):
            return JsonResponse({'message':'INVAILD PHONE_ERROR'}, status=400)
           
        if len(login_pw) < PW_LENGTH:
            return JsonResponse({'message':'INVAILD PW_ERROR'}, status=400)

        if User.objects.filter(nickname = nickname).exists():
            return JsonResponse({'message':'NICKNAME DUPLICATE_ERROR'}, status=400)
        
        if User.objects.filter(email = login_id).exists():
            return JsonResponse({'message':'ID DUPLICATE_ERROR'}, status=400)
        
        if User.objects.filter(phone = phone).exists():
            return JsonResponse({'message':'PHONE DUPLICATE_ERROR'}, status=400)

        hash_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt() )
        User.objects.create(
                    email    = data['email'],
                    password = hash_password.decode('utf-8') ,
                    nickname = data['nickname'],
                    name     = data['name'],
                    phone    = data['phone'] )

        return JsonResponse({'message':'SUCCESS'}, status=200)


class LoginView(View):
    def post(self, request):
        data        = json.loads(request.body)
        user_input  = data['id']
        login_pw    = data['password']

        if user_input == '' or login_pw == '' :
                return JsonResponse({'message':'KEY_ERROR'}, status= 400)

        elif User.objects.filter(email=user_input).exists():
                login_id = User.objects.get(email=user_input)
        
        elif User.objects.filter(phone=user_input).exists():
                login_id = User.objects.get(phone=user_input)
        
        elif User.objects.filter(nickname=user_input).exists():
                login_id = User.objects.get(nickname=user_input)

        else:
                return JsonResponse({'message':'INVALID_ID'}, status = 404) 


        if bcrypt.checkpw(login_pw.encode('utf-8'), login_id.password.encode('utf-8') ):
                return JsonResponse({'message':'SUCCESS'}, status = 200)
        
        return JsonResponse({'message':'INVALID_PW'}, status = 401)