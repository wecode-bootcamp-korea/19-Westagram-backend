import json

from django.http    import JsonResponse
from django.views   import View

from .models        import User

class SignUpView(View):
    def post(self, request):
        data        = json.loads(request.body)
        user_name   = data['user_name']
        email       = data['email']
        password    = data['password']
        phone_num   = data['phone_num']

