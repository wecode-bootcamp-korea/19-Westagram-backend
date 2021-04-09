from django.shortcuts import render
import json, base64
from django.http                import JsonResponse
from django.core.exceptions     import ValidationError
from django.views               import View
from django.db.models           import Q
from .models                    import Posting

class PostingView(View):
    def post(self,request):

class DisplayView(View):
    def post(self,request):




