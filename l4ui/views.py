#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests, json
from django.http import HttpResponse

# Create your views here.

@login_required(login_url='/login')
def create_l4(request):
    return render(request, 'l4ui/create_l4.vue', {})


@login_required(login_url='/login')
def l4check(request):
    BASE_URL = 'http://i-php-iapi.skplanet.com/l4check/check_json.php?'
    r = requests.get(BASE_URL + 'ip=' + request.GET['ip'])

    # 비정상 IP 입력시 ${sIDC}-php-iapi의 결과는 "Please give me a valid IP Address\n"
    if r.text[:-1] == "Please give me a valid IP Address":
        return HttpResponse("정상적인 IP를 입력해주세요.")

    try:
        vip_list = json.loads(r.text).keys()
    except:
        return HttpResponse("정상적인 IP를 입력해주세요.")

    if vip_list != []:
        return HttpResponse("해당 Virtual IP는 사용 불가능 합니다.")
    else:
        return HttpResponse("해당 Virtual IP는 사용 가능 합니다.", content_type="application/json")


@login_required(login_url='/login')
def test(request):
    return render(request, 'l4ui/test.vue', {})
