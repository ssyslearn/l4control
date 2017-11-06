{% extends 'l4ui/base.html' %}

{% block content %}
<div class="container">
    <div class="row home-intro text-center">

        <h2 class="tagline">L4 생성</h2>
        <hr class="small">

        <div id="test"></div>

    </div>
</div>
<div id="container" class="container">
    <div class="row-mid" style="margin-left: 300px; margin-right: 300px; ">
        <div class="col-md-12">
            <label class="label-title">Virtual IP</label>
        </div>
        <div id="assign_vip">
            <div class="col-md-8">
                <input type="text" v-model="input_vip" placeholder="Virtual IP" required="" class="form-control input-lg">
                <p> ${ input_vip } </p>
            </div>
            <div class="col-md-4" >
                <button v-on:click="assign" class="btn btn-lg btn-info" >IP 할당</button>
            </div>
        </div>
        
        <div id="service_name">
            <div class="col-md-12">
                <label class="label-title">서비스 명</label>
            </div>
            <div class="col-md-8">
                <input v-model="input_service_name" type="text"  placeholder="서비스명을 입력하세요" required="" class="form-control input-lg" >
                <p> ${ input_service_name } </p>
            </div>
            <div class="col-md-4">
                <!--
                <label class="label-title">v_${ srv_input_vip }_${ input_service_name }_port</label>
                -->
            </div>
            <div class="col-md-12"><br></div>
        </div>


        <div class="col-md-12">
            <label class="label-title" id="label_virtual_port">Virtual Server</label>
            <button class="btn btn-xs btn-info">+</button>
            <div class="col-md-round-box">
                <div class="col-md-4">
                    <div class="col-md-12">
                        <label class="label-title" id="label_virtual_port">Virtual Port</label>
                    </div>
                    <div class="col-md-round-box">
                        <div class="col-md-12-inner">
                            <label class="label-subtitle">Port</label>
                            <input type="text" id="rip" placeholder="ex. 80" required="" class="form-control input-lg">
                        </div>
                        <div class="col-md-12-inner">
                            <label class="label-subtitle">Sticky 사용 여부</label>
                            <select class="form-control input-md" id="sel1">
                                <option>사용 안함</option>
                                <option>300초</option>
                                <option>600초</option>
                                <option>900초</option>
                                <option>1800초</option>
                            </select>
                        </div>

                        <div class="col-md-12-inner">
                            <label class="label-subtitle">DSR 사용 여부</label>
                            <select class="form-control input-md" id="sel1">
                                <option>사용 안함</option>
                                <option>사용</option>
                            </select>
                        </div>
                        <div class="col-md-12-inner">
                            <label class="label-subtitle">SSL 인증서 사용 여부 </label>
                            <select class="form-control input-md" id="sel1">
                                <option>사용 안함</option>
                                <option>사용</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="col-md-12">
                        <label class="label-title" id="label_real_server">Real Server</label>
                        <button class="btn btn-xs btn-info">+</button>
                    </div>
                    <div class="col-md-round-box">

                        <div class="col-md-4">
                            <label class="label-subtitle">Real IP</label>
                            <input type="text" id="sticky" placeholder="ex. 10.10.1.1" required="" class="form-control input-md">
                        </div>
                        <div class="col-md-2">
                            <label class="label-subtitle">Port</label>
                            <input type="text" id="sticky" placeholder="ex. 80" required="" class="form-control input-md">
                        </div>
                        <div class="col-md-2">
                            <label class="label-subtitle">LB mode</label>
                            <select class="form-control input-md" id="sel1">
                                <option>Round Robin</option>
                                <option>Least Connections</option>
                            </select>
                        </div>
                        <div class="col-md-3">
                            <label class="label-subtitle">Monitor</label>
                            <select class="form-control input-md" id="sel1">
                                <option>http_healthcheck.jsp_skphok</option>
                                <option>tcp</option>
                                <option>tcp_half_open</option>
                                <option>icmp</option>
                                <option>udp</option>
                            </select>
                        </div>

                    </div>
                </div>
            </div>
        </div>


        <div class="col-md-12" align="right">
            <button class="btn btn-success btn-lg" id="get-checked-data">확인</button>
            <input id="create_button" type="button" class="btn btn-lg btn-success" value="생성" onclick="vip_create();" disabled/>
        </div>

        <div class="col-md-12">
            <pre id="display-json"></pre>
        </div>
    </div>

</div>


<input type="text" v-model="test" placeholder="Virtual IP" required="" class="form-control input-lg">
<p v-text="test"></p>

<script src="/static/js/jquery/1.11.3/jquery.min.js"></script>
<script src="/static/js/jquery.redirect.js"></script>
<link href="/static/css/l4style.css" rel="stylesheet" type="text/css">
<script src="/static/js/vue.js"></script>


<script>

    Vue.options.delimiters = ['${', '}'];

    var assign_vip = new Vue({
        el: '#assign_vip',
        data: {
            input_vip: ''
        },
        // 메소드는 `methods` 객체 안에 정의합니다
        methods: {
            assign: function (event) {
                // 메소드 안에서 사용하는 `this` 는 Vue 인스턴스를 가리킵니다
                alert('Hello ' + this.input_vip + '!')
            }
        }
    })

    var service_name = new Vue({
        el: '#service_name',
        data: {
            input_service_name: ''
        }
    })


</script>

{% endblock %}
