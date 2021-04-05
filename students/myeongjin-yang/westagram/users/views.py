import json
import re

from django.http  import JsonResponse
from django.views import View 

from users.models import User

class SignUpView(View):
    def post(self,request):
        data               = json.loads(request.body)
        email_check        = re.compile('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')
        phonenumber_check  = re.compile('[0-9]{3}[0-9]{4}[0-9]{4}')

        try:
            identity       = data['identity']
            password       = data['password']
            name           = data['name']
            username       = data['username']

            if not email_check.match(identity) and not phonenumber_check.match(identity):
                return JsonResponse({'message':"Invalid ID"}, status=400)
                        
            elif len(password)<8:
                return JsonResponse({'message':"Invalid PW"}, status=400)

            elif User.objects.filter(username=username):
                return JsonResponse({'message':"existing username"}, status=400)
            
            elif User.objects.filter(identity=identity):
                return JsonResponse({'message':"existing ID"}, status=400)
            
            else:
                User.objects.create(identity=data['identity'], password=data['password'], name=data['name'], username=data['username'])
        
        except KeyError:
            return JsonResponse({'message':"KEY_ERROR"}, status=400)
        else:
            return JsonResponse({'message':"SUCCESS"}, status=200)

class SignInView(View):
    def post(self,request):
        data               = json.loads(request.body)
        try:
            indentity          = data['identity']
            password           = data['password']

        
        
