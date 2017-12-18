#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests, json
from django.http import HttpResponse

# Create your views here.

L4_URL = []

@login_required(login_url='/login')
def create_l4(request):
    return render(request, 'l4ui/create_l4.vue', {})

@login_required(login_url='/login')
def modify_l4(request):
    return render(request, 'l4ui/modify_l4.vue', {'ip': request.GET['ip']})


@login_required(login_url='/login')
def verify_vip(request):
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

        #if vip_list != [] or len(vip_list) == 0:
        if vip_list != [] or len(vip_list) != 0:
            return HttpResponse(json.dumps({"data": "[WARNING] 해당 Virtual IP는 사용 불가능 합니다.", "status": "404"}))
        else:
            return HttpResponse(json.dumps({"data": "[OK] 해당 Virtual IP는 사용 가능 합니다.", "status": "200"}))

    return HttpResponse(json.dumps({"data": "정상적인 IP를 입력해주세요.", "status": "500"}))

@login_required(login_url='/login')
def search_l4check(request):
    for url in L4_URL:
        BASE_URL = url + 'check_json.php?'
        l4_dict = {}
        try:
            r = requests.get(BASE_URL + 'ip=' + request.GET['ip'], timeout=2)
        except:
            continue

        # 비정상 IP 입력시 ${sIDC}-php-iapi의 결과는 "Please give me a valid IP Address\n"
        if r.text[:-1] == "Please give me a valid IP Address":
            continue

        if r.text == '{}':
            continue

        try:
            for el in json.loads(r.text):
                l4_dict[el] = json.loads(r.text)[el]
        except:
            continue

        if l4_dict != {} or len(l4_dict.keys()) != 0:
            return HttpResponse(json.dumps({"data": l4_dict, "status": "200"}))
        else:
            return HttpResponse(json.dumps({"data": {}, "status": "200"}))


    return HttpResponse(json.dumps({"data": "정상적인 IP를 입력해주세요.", "status": "500"}))


# 아래의 l4map 함수는 추후 API G/W에서 캐싱한 데이터를 사용하는 것이 좋아보임
# IN : Virutal IP, OUT : L4 Name, L4 IP
@login_required(login_url='/login')
def search_matched_dev(request):
    l4map_list = []
    selected_dev = ''
    for url in L4_URL:
        BASE_URL = url + 'F5Map.txt'
        try:
            r= requests.get(BASE_URL, timeout=2)
            try:
                r_list = r.text.split('\n')
                for el in r_list:
                    if len(el) != 0:
                        l4map_list.append(el.split('\t'))
            except:
                continue
        except:
            continue

    vip_range = '.'.join(request.GET['vip'].split('.')[:-1])

    # 아래는 순차탐색이므로 추후 이진탐색으로 변경해야함
    l4map_gen = iter(l4map_list)
    # print l4map_list

    for l4_el in l4map_gen:
        try:
            if vip_range == '.'.join(l4_el[-2].split('.')[:-1]):
                # print [l4_el[0], l4_el[1],l4_el[-2]]
                selected_dev = [l4_el[0], l4_el[1]]
                return HttpResponse(json.dumps({"data": selected_dev, "status": "200"}))
        except:
            print 'error in' + l4_el

    return HttpResponse("매칭되는 L4 장비가 없습니다.")



# IN : Virtual IP, OUT : New Virtual IP
@login_required(login_url='/login')
def search_usable_vip(request):
    l4map_list = []
    used_vip = []
    usable_vip = ''
    for url in L4_URL:
        BASE_URL = url + 'F5Map.txt'
        try:
            r= requests.get(BASE_URL, timeout=2)
            try:
                r_list = r.text.split('\n')
                for el in r_list:
                    if len(el) != 0:
                        l4map_list.append(el.split('\t'))
            except:
                continue
        except:
            continue

    vip_range = '.'.join(request.GET['vip'].split('.')[:-1])

    # 아래는 순차탐색이므로 추후 이진탐색으로 변경해야함
    l4map_gen = iter(l4map_list)
    # print l4map_list

    for l4_el in l4map_gen:
        try:
            # F5Map에서 VIP를 기준으로만 검색하므로 RIP가 vip_range로 들어와도 상관은 없으나...
            # 특정 VIP와 RIP가 같은 대역인 경우 문제가 발생함 ( ex. 10.10.100.0 대역 )
            # To Do ...
            if vip_range == '.'.join(l4_el[-2].split('.')[:-1]):
                # print [l4_el[0], l4_el[1],l4_el[-2]]
                used_vip.append(l4_el[-2].split(':')[0])
        except:
            print 'error in' + l4_el

    if used_vip:
        if request.GET['vip'] not in used_vip:
            usable_vip = request.GET['vip']
        else:
            for i in range(21, 226):
                cmp_ip = vip_range + ".%s" % (i)
                if cmp_ip not in used_vip:
                    usable_vip = cmp_ip
                    break

        return HttpResponse(json.dumps({"data": usable_vip, "status": "200"}))
    else:
        # print selected_dev
        # return HttpResponse(json.dumps(usable_vip))
        return HttpResponse(json.dumps({"data": "올바른 대역의 Virtual IP를 입력해주세요.", "status": "404"}))

    return HttpResponse(json.dumps({"data": "잘못된 요청입니다. 다시 확인해주세요.", "status": "500"}))


@login_required(login_url='/login')
def test(request):
    return render(request, 'l4ui/test.vue', {})
