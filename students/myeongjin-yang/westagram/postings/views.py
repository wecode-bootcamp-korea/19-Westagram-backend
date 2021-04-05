import json

from django.http     import JsonResponse
from django.views    import View

from postings.models import Posting

class PostAddView(View):
    def post(self,request):
        data               = json.loads(request.body)
        image_url          = data['image_url']
        username           = data['username']

        