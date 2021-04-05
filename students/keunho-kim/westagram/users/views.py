import json
from django.http      import JsonResponse
from django.views     import View
from users.models     import User
# Create your views here.

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        User.objects.create(id=data['id'], email=data['email'], password=data['password'])




        return JsonResponse({'message': 'Success!'}, status=200)

class LogInView(View):
     def post(self, request):
        data = json.loads(request.body)
