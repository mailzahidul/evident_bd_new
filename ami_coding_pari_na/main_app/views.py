from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user_admin.models import User
from datetime import datetime
from .models import InputValue
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import InputValueSerializer
import requests
from django.http import Http404
from django.contrib import messages
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
import requests, json
# Create your views here.

def get_auth_token(obj):
    token = Token.objects.get_or_create(user=obj)
    return token


@login_required
def home(request):
    context={}
    datetime_format = '%d-%m-%Y %H:%M:%S'
    login_user = request.user
    user_id = User.objects.get(email=login_user)
    user_list = User.objects.all()
    context['user_list'] = user_list
    full_token = get_auth_token(login_user)
    string_token = str(full_token)
    token = string_token.split(' ')[1][:-2]
    result = ''
    url = 'http://127.0.0.1:8001/list_input_values'
    if request.method == 'POST':
        timestamp = datetime.now().strftime(datetime_format)
        input_values = request.POST['input_items']
        numbers = [int(i) for i in input_values.split(',')]
        search_value = request.POST['search_value']
        if int(search_value) in numbers:
            result = True
        else:
            result = False
        numbers.sort(reverse=True)
        InputValue.objects.create(user=user_id, timestamp=timestamp, input_values=numbers)
    context['result'] = result
    
    if 'from_datetime' and 'to_datetime' in request.GET:
        u = request.GET.get('user')
        user = User.objects.get(id=u)
        from_datetime = request.GET['from_datetime']
        to_datetime = request.GET['to_datetime']
        header = {"Authorization": f'Token {token}'}
        response = requests.get(url, headers=header, data={"user":user.email,"start_date_str":from_datetime, "end_date_str":to_datetime}).json()
        context['input_values'] = response
    return render(request, 'index.html', context)


class ShowInputValueView(APIView):
    permissions_classes = [IsAuthenticated]
    def get(self, request):
        user_data = request.data['user']
        user = User.objects.get(email=user_data)
        start_date_str = request.data['start_date_str']
        end_date_str = request.data['end_date_str']

        input_values = InputValue.objects.filter(user=user, timestamp__gte=start_date_str, timestamp__lte=end_date_str)
        if not input_values:
            return Response({"status": False, "message": 'No Object', "code": 400})
        serializer = InputValueSerializer(input_values, many=True)
        return Response({"status": 'success',"user_id": user.id , "payload": serializer.data})
