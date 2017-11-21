#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests, json
from django.http import HttpResponse

# Create your views here.

L4_URL = ['http://c-php-iapi.skplanet.com/l4check/', 'http://b-php-iapi.skplanet.com/l4check/', 'http://i-php-iapi.skplanet.com/l4check/']
#L4_URL = ['http://i-php-iapi.skplanet.com/l4check/']

@login_required(login_url='/login')
def create_l4(request):
    return render(request, 'l4ui/create_l4.vue', {})


@login_required(login_url='/login')
def l4check(request):
    for url in L4_URL:
        BASE_URL = url + 'check_json.php?'
        try:
            r = requests.get(BASE_URL + 'ip=' + request.GET['ip'], timeout=2)
        except:
            continue

        # 비정상 IP 입력시 ${sIDC}-php-iapi의 결과는 "Please give me a valid IP Address\n"
        if r.text[:-1] == "Please give me a valid IP Address":
            continue

        try:
            vip_list = json.loads(r.text).keys()
        except:
            continue

        if vip_list != []:
            return HttpResponse(json.dumps({"data": "[WARNING] 해당 Virtual IP는 사용 불가능 합니다.", "status": "404"}))
        else:
            return HttpResponse(json.dumps({"data": "[OK] 해당 Virtual IP는 사용 가능 합니다.", "status": "200"}))

    return HttpResponse(json.dumps({"data": "정상적인 IP를 입력해주세요.", "status": "500"}))


# 아래의 l4map 함수는 추후 API G/W에서 캐싱한 데이터를 사용하는 것이 좋아보임
@login_required(login_url='/login')
def l4map(request):
    for url in L4_URL:
        BASE_URL = url + 'F5Map.txt'
        l4map_list = []

        try:
            r= requests.get(BASE_URL, timeout=2)
        except:
            continue
        try:
            r_list = r.text.split('\n')
            for el in r_list:
                l4map_list.append(el.split('\t'))

            selected_dev = ''
            vip_range = '.'.join(request.GET['ip'].split('.')[:-1])
            # 아래는 순차탐색이므로 추후 이진탐색으로 변경해야함
            for l4_el in l4map_list:
                if vip_range == '.'.join(l4_el[-2].split('.')[:-1]):
                    selected_dev = [l4_el[0], l4_el[1]]
                    break
            return HttpResponse(json.dumps(selected_dev))
        except:
            continue

    return HttpResponse("매칭되는 L4 장비가 없습니다.")


@login_required(login_url='/login')
def test(request):
    return render(request, 'l4ui/test.vue', {})
