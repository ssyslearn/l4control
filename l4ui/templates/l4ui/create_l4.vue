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

        <div id="virtual_server">
            <div>
                <div class="col-md-12">
                    <label class="label-title">서비스 명</label>
                </div>
                <div class="col-md-8">
                    <input v-model="input_service_name" type="text"  placeholder="서비스명을 입력하세요" required="" class="form-control input-lg" >
                    <!--<span class="label-svctitle" v-for="index in vs_count" v-model="virtual_port[0]">-->
                    <span class="label-svctitle" v-for="index in virtual_port">
                          <!--v_${ input_vip }_${ input_service_name }_${ port },-->
                          v_${ input_vip }_${ input_service_name }_${ index.virtual_port },
                      </span>
                </div>
                <div class="col-md-12"><br></div>
            </div>

            <div class="col-md-12">
                <label class="label-title">Virtual Server</label>
                <button v-on:click="add_vs" class="btn btn-xs btn-info">+</button>
                <div v-bind:id="`vs-box-${ index }`" v-for="index in vs_count">
                    <virtual-server-box></virtual-server-box>
                </div>
            </div>
        </div>



        <div id="display_config" class="col-md-12" align="right">
            <button class="btn btn-success btn-lg" v-on:click="click_display">확인</button>
            <input type="button" class="btn btn-lg btn-success" value="생성" disabled/>
            <div class="col-md-12" align="left"><br>
                <pre>
                <display-config></display-config>
            </pre>
            </div>
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
        virtual_port: [{'virtual_port': '', 'real_count': '', 'real_server_ip': '', 'real_server_port': '', 'real_server_lb_mode': '', 'real_server_monitor':'' , 'sticky': '', 'dsr': '', 'ssl': ''}]
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


    Vue.component('virtual-server-box', {
        props: [],
        data: function() {
            return {
                vs_box_count: this.$parent.vs_count,
                vs_box_port: '',
                real_count: 1,
                real_server_ip: '',
                sticky: '',
                dsr: '',
                ssl: '',
                real_server_port: '',
                real_server_lb_mode: '',
                real_server_monitor: ''
            }
        },
        methods: {
            changed: function (){
                // passing to parent
                this.$parent.virtual_port[this.vs_box_count-1]['virtual_port'] = this.vs_box_port;
                this.$parent.virtual_port[this.vs_box_count-1]['real_count'] = this.real_count;
                this.$parent.virtual_port[this.vs_box_count-1]['real_server_ip'] = this.real_server_ip;
                this.$parent.virtual_port[this.vs_box_count-1]['sticky'] = this.sticky;
                this.$parent.virtual_port[this.vs_box_count-1]['dsr'] = this.dsr;
                this.$parent.virtual_port[this.vs_box_count-1]['ssl'] = this.ssl;
                this.$parent.virtual_port[this.vs_box_count-1]['real_server_port'] = this.real_server_port;
                this.$parent.virtual_port[this.vs_box_count-1]['real_server_lb_mode'] = this.real_server_lb_mode;
                this.$parent.virtual_port[this.vs_box_count-1]['real_server_monitor'] = this.real_server_monitor;
            }
        },
        template: '<div class="col-md-round-box">' +
        '<div class="col-md-4"> ' +
        '<div class="col-md-12"><label class="label-title">Virtual Port</label></div> ' +
        '<div class="col-md-round-box">' +
        '<div class="col-md-12-inner" >' +
        '<label class="label-subtitle">Port</label> ' +
        '<input type="text" placeholder="ex. 80" required="" class="form-control input-lg" v-model="vs_box_port" v-on:change="changed">' +
        '</div> ' +
        '<div class="col-md-12-inner">' +
        '<label class="label-subtitle">Sticky 사용 여부</label><select v-model="sticky" v-on:change="changed" class="form-control input-md"> ' +
        '<option>사용 안함</option><option>300초</option> <option>600초</option> <option>900초</option> <option>1800초</option> ' +
        '</select>' +
        '</div>' +
        '<div class="col-md-12-inner"><label class="label-subtitle">DSR 사용 여부</label> ' +
        '<select v-model="dsr" v-on:change="changed" class="form-control input-md"> <option>사용 안함</option> <option>사용</option> </select>' +
        '</div> ' +
        '<div class="col-md-12-inner">' +
        '<label class="label-subtitle">SSL 인증서 사용 여부 </label><select v-model="ssl" v-on:change="changed" class="form-control input-md" id="sel1"> ' +
        '<option>사용 안함</option> <option>사용</option> </select>' +
        '</div>' +
        '</div>' +
        '</div> ' +
        '<div class="col-md-8">' +
        '<div class="col-md-12">' +
        '<div class="col-md-12">' +
        '<label class="label-title" id="label_real_server">Real Server</label> ' +
        '</div>'+
        '<div class="col-md-12">' +
        '<div class="col-md-2">' +
        '<label class="label-subtitle">Port</label><input type="text" v-model="real_server_port" v-on:change="changed" placeholder="ex. 80" required="" class="form-control input-md"> ' +
        '</div>' +
        '<div class="col-md-2">' +
        '<label class="label-subtitle">LB mode</label>' +
        '<select v-model="real_server_lb_mode" v-on:change="changed"  class="form-control input-md" > ' +
        '<option>Round Robin</option> <option>Least Connections</option> </select>' +
        '</div> ' +
        '<div class="col-md-3">' +
        '<label class="label-subtitle">Monitor</label>' +
        '<select v-model="real_server_monitor" v-on:change="changed"  class="form-control input-md" > ' +
        '<option>http_healthcheck.jsp_skphok</option> <option>tcp</option> <option>tcp_half_open</option> <option>icmp</option> ' +
        '<option>udp</option> </select>' +
        '</div>' +
        '</div>' +
        '<div class="col-md-12">' +
        '<label class="label-subtitle">Real IP</label> ' +
        '<textarea v-model="real_server_ip" v-on:change="changed" name="content"  placeholder="ex. 10.10.10.10" required="" class="form-control input-md" cols="40" rows="4" >' +
        '</textarea>' +
        '</div> ' +
        '</div>' +
        '</div>' +
        '</div>'
    })



    var virtual_server = new Vue({
        el: '#virtual_server',
        data: data,
        methods: {
            add_vs: function (event) {
                if (this.vs_count < 5) {
                    this.vs_count += 1;
                    this.virtual_port.push({'virtual_port': '', 'real_count': '', 'real_server_ip': '', 'real_server_port': '', 'real_server_lb_mode': '', 'real_server_monitor':'' , 'sticky': '', 'dsr': '', 'ssl': ''});
                }
            }
        }
    })

    Vue.component('display-config', {
        props: ['virtual_port'],
        data: function() {
            return {
                display_virtual_port: this.$parent.virtual_port
            }
        },
        template: '<div>virtual_server <br> ${ display_virtual_port }</div>'
    })

    var display_config = new Vue({
        el: '#display_config',
        data: data,
        methods: {
            click_display: function (event) {

            }
        }
    })
</script>

{% endblock %}
