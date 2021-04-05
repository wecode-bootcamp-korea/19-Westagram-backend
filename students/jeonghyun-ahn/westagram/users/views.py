import json, re
from .models            import User
from django.db.models   import aggregates
from django.http        import JsonResponse
from django.views       import View

class UserView(View):
    def post(self, request):
        data        = json.loads(request.body)
        id_1        = data['email']
        input2      = data['password']
        nickname    = data['nickname']
        phone_check = re.compile('^[0-9]{3}[0-9]{3,4}[0-9]{4}')
        email_check = re.compile('^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$')


        if len(id_1) <= 0 or len(input2) == 0 :
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

        elif not email_check.match(id_1) and not phone_check.match(id_1):
                return JsonResponse({'message':'Invaild ID_ERROR'}, status=400)
           
        elif len(input2) < 8:
                return JsonResponse({'message':'Invaild PW_Error'}, status=400)

        elif User.objects.filter(nickname=nickname):
                return JsonResponse({'message':'Nickname Duplicate_Error'}, status=400)
        
        elif User.objects.filter(email=id_1):
                return JsonResponse({'message':'ID Duplicate_Error'}, status=400)

        User.objects.create(
                    email   = data['email'],
                    password= data['password'],
                    nickname= data['nickname'],
                    name    = data['name'])
        return JsonResponse({'message':'SUCCESS'}, status=200)
