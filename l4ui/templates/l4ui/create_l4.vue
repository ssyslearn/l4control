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
                    <!--<span class="label-svctitle" v-for="index in vs_count" v-model="virtual_port[0]">-->
                    <span class="label-svctitle" v-for="index in vs_count">
                        <!--v_${ input_vip }_${ input_service_name }_${ port },-->
                        v_${ input_vip }_${ input_service_name }_${ virtual_port[index] },
                    </span>
                </div>
                <div class="col-md-12"><br></div>
            </div>

            <div id="virtual_server" class="col-md-12">
                <label class="label-title">Virtual Server</label>
                <button v-on:click="add_vs" class="btn btn-xs btn-info">+</button>
                <div v-bind:id="`vs-box-${ index }`" v-for="index in vs_count">
                <!--<div v-bind:id="`vs-box-${ vport }`" v-for="vport in virtual_port">-->
                    <virtual-server-box></virtual-server-box>
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

<script src="/static/js/jquery/1.11.3/jquery.min.js"></script>
<script src="/static/js/jquery.redirect.js"></script>
<link href="/static/css/l4style.css" rel="stylesheet" type="text/css">
<script src="/static/js/vue.js"></script>


<script>

    Vue.options.delimiters = ['${', '}'];

    var data = {
        vs_count: 1,
        input_vip: '',
        input_service_name: '',
        virtual_port: []
    }

    var assign_vip = new Vue({
        el: '#assign_vip',
        data: data,
        methods: {
            assign: function (event) {
                alert('Hello ' + this.input_vip + '!')
            }
        }
    })

    var service_name = new Vue({
        el: '#service_name',
        data: data
    })


    var virtual_server_box = {
            props: ['virtual_port'],
            data: function() {
                return {
                    vs_box_port: this.virtual_port
                }
            },
            template: '<div class="col-md-round-box">' +
            '<div class="col-md-4"> ' +
            '<div class="col-md-12"><label class="label-title">Virtual Port</label></div> ' +
            '<div class="col-md-round-box">' +
            '<div class="col-md-12-inner" >' +
            '<label class="label-subtitle">Port</label> ' +
            '<input type="text" placeholder="ex. 80" required="" class="form-control input-lg" v-model="vs_box_port">' +
            '</div> ' +
            '<div class="col-md-12-inner">' +
            '<label class="label-subtitle">Sticky 사용 여부</label><select class="form-control input-md" id="sel1"> ' +
            '<option>사용 안함</option><option>300초</option> <option>600초</option> <option>900초</option> <option>1800초</option> ' +
            '</select>' +
            '</div>' +
            '<div class="col-md-12-inner"><label class="label-subtitle">DSR 사용 여부</label> ' +
            '<select class="form-control input-md" id="sel1"> <option>사용 안함</option> <option>사용</option> </select>' +
            '</div> ' +
            '<div class="col-md-12-inner">' +
            '<label class="label-subtitle">SSL 인증서 사용 여부 </label><select class="form-control input-md" id="sel1"> ' +
            '<option>사용 안함</option> <option>사용</option> </select>' +
            '</div>' +
            '</div>' +
            '</div> ' +
            '<div class="col-md-8">' +
            '<div class="col-md-12">' +
            '<label class="label-title" id="label_real_server">Real Server</label> ' +
            '<button class="btn btn-xs btn-info">+</button>' +
            '</div>' +
            '<div class="col-md-round-box"> ' +
            '<div class="col-md-4">' +
            '<label class="label-subtitle">Real IP</label> ' +
            '<input type="text" id="sticky" placeholder="ex. 10.10.1.1" required="" class="form-control input-md">' +
            '</div> ' +
            '<div class="col-md-2">' +
            '<label class="label-subtitle">Port</label><input type="text" id="sticky" placeholder="ex. 80" required="" class="form-control input-md"> ' +
            '</div>' +
            '<div class="col-md-2">' +
            '<label class="label-subtitle">LB mode</label> <select class="form-control input-md" id="sel1"> ' +
            '<option>Round Robin</option> <option>Least Connections</option> </select>' +
            '</div> ' +
            '<div class="col-md-3">' +
            '<label class="label-subtitle">Monitor</label> <select class="form-control input-md" id="sel1"> ' +
            '<option>http_healthcheck.jsp_skphok</option> <option>tcp</option> <option>tcp_half_open</option> <option>icmp</option> ' +
            '<option>udp</option> </select>' +
            '</div>' +
            '</div>' +
            '</div>' +
            '</div>',

    }

    var virtual_server = new Vue({
        el: '#virtual_server',
        data: data,
        components: {
            'virtual-server-box' : virtual_server_box
        },
        methods: {
            add_vs: function (event) {
                if (this.vs_count < 5) {
                    this.vs_count += 1;
                    //alert(this.$el.getElementsByClassName("vport_class")[this.vs_count-1].text);
                    //this.virtual_port.push(this.$el.getElementsByClassName("vport_class")[this.vs_count-1].value);
                    //this.virtual_port = assign_vport.virtual_port;
                    this.virtual_port = this.$children;
                }
            }
        }
    })

    var assign_vport = new Vue({
        el: '#assign_vport',
        data: data,
        methods: {
            changed: function(){
                alert(10);
            }
        }
    })

</script>

{% endblock %}
