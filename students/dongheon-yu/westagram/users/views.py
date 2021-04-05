import json

from django.http  import JsonResponse # 통신
from django.views import View # views.py에서 import 
from .models      import User # models.py에서 User class import


#     <post 보낼 때 순서>
# 1. 일단 첫 번째 조건. httpie 통신으로 데이터가 들어올 때, 이메일이나 패스워드 둘 중에 하나라도 없으면 에러가 발생해야 한다. 
# return JsonResponse("message": "KEY_ERROR"}, status code 400)
# 어차피 가입이 안되면 밑의 코드가 실행이 안되면 되니까, 이 조건을 가장 위로 올린다

# 2. 가입할 때, 이메일 주소가 기존의 이메일 주소와 같으면 가입이 될 수 없다. 2번째 조건으로 처리한다. 

#     <email, password validation>
# 3. 회원가입 시, email, password 중에서, email 에는 @가 들어갔는지 검사해야 한다. 
# 만약에 @가 없는 이메일 형식이라면 가입이 승인되지 않는다

# 4. 3번과 마찬가지로, password가 5글자 이상이 아니고 이하라면 가입이 되지 않는다

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        email       = data['email']
        name        = data['name']
        phoneNumber = data['phoneNumber']
        password    = data['password']

        if not (email or password):
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
      
        try:
            if User.objects.filter(email = data['email']).exists() == True:
                return JsonResponse({"message" : "같은 아이디가 존재합니다."}, status = 401)
        except:
            pass

        if ('@' or '.') not in email:
            return JsonResponse({"message" : "아이디를 제대로 써주세요"}, status = 401)

#        user_id = User.objects.get([data['email']])
#        if user_id not in '@':
#            return JsonResponse({"message" : "아이디를 제대로 써주세요"}, status = 401)
# 4.    
        if len(password) < 6:
            return JsonResponse({"message" : "비밀번호를 5글자 이상으로 늘려주세요"}, status = 401)
# 5.
        else:
            User.objects.create(
                    email       = data['email'],
                    name        = data['name'],
                    phoneNumber = data['phoneNumber'],
                    password    = data['password']
            )
            return JsonResponse({"message" : "Success"}, status = 200)
