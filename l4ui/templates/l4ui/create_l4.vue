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
                <!--<button id="show-modal" @click="showModal = true" v-on:click="assign" class="btn btn-lg btn-info" >IP 할당</button>-->
                <button id="show-modal" @click="showModal = true" class="btn btn-lg btn-info" >IP 할당</button>
                  <!-- use the modal component, pass in the prop -->
                  <modal v-if="showModal" v-on:close="set_vip()">
                    <!--
                      you can use custom content here to overwrite
                      default content
                    -->
                      <!--<input type="text" placeholder="Real IP" required="" class="form-control input-lg">-->
                      <!--<button v-on:click="assign" class="btn btn-lg btn-info" >IP 할당</button>-->

                      <h3 slot="header">Virtual IP 할당</h3>
                      <div slot="body">
                          <div style="text-align: center;">
                            L4에 등록할 Real IP 혹은 사용할 Virutal IP를 입력해주세요
                                <br><br>
                            <input type="text" v-model="input_rip" placeholder="IP" required="" class="form-control input-lg" style="width: 30%; margin: 0 auto; display: inline;">
                                <input id="search_btn" type="button" class="btn-lg btn-info" value="조회" v-on:click="click_search_btn"/>
                            </div>
                      </div>

                      <div slot="footer">
                          <div class="row-mid">
                    <div class="container">
                        <table class="table table-striped">
                            <thead>
                            <tr>
                                <th>Virtual Name</th>
                                <th>Virtual IP</th>
                                <th>Port</th>
                                <th>Pool Name</th>
                                <th>Pool Member</th>
                                <th>LB Mode</th>
                                <th>Sticky</th>
                                <th>translate<br>Address</th>
                                <th>Monitor</th>
                                <th>선택</th>
                            </tr>
                            </thead>
                            <tbody is="lb-table-box" v-bind:vs_list="vs_list">
                            </tbody>
                        </table>
                    </div>
                </div>

                <button class="modal-default-button" @click="set_vip()">
                    OK
                </button>
                      </div>

                  </modal>
            </div>
        </div>

        <div id="virtual_server">
            <div>
                <div class="col-md-12">
                    <label class="label-title">서비스 명</label>
                </div>
                <div class="col-md-8">
                    <input :disabled="writable == false" v-model="input_service_name" type="text"  placeholder="서비스명을 입력하세요" required="" class="form-control input-lg" >
                    <!--<span class="label-svctitle" v-for="index in vs_count" v-model="virtual_port[0]">-->
                    <span class="label-svctitle" v-for="index in virtual_port_list">
                          <!--v_${ input_vip }_${ input_service_name }_${ port },-->
                          v_${ input_vip }_${ input_service_name }_${ index.virtual_port },
                      </span>
                </div>
                <div class="col-md-12"><br></div>
            </div>
            <div class="col-md-12">
                <label class="label-title">Virtual Server</label>
                <button v-on:click="add_vs" class="btn btn-xs btn-info">+</button>
                <div>
                    <virtual-server-box v-bind:id="`vs-box-${ index }`" v-for="(vs,index) in virtual_port_list" v-on:delete-vs="delete_this_vs(index)"></virtual-server-box>
                </div>
            </div>
        </div>

        <div id="display_config" class="col-md-12" align="right">
            <button v-if="confirm_btn_seen" class="btn btn-success btn-lg" v-on:click="click_display">확인</button>
            <input :disabled="create_btn_seen == false" type="button" class="btn btn-lg btn-success" value="생성" />
            <div class="col-md-12" align="left"><br>
                <pre v-if="display_seen">
                    <display-config></display-config>
                </pre>
            </div>
        </div>
    </div>
</div>



<script src="/static/js/jquery/1.11.3/jquery.min.js"></script>
<script src="/static/js/jquery.redirect.js"></script>
<link href="/static/css/l4style.css" rel="stylesheet" type="text/css">
<link href="/static/css/modal.css" rel="stylesheet" type="text/css">
<script src="/static/js/vue.js"></script>
<script src="/static/js/axios.min.js"></script>

<script type="text/x-template" id="modal-template">
  <transition name="modal">
    <div id="" class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-header">
            <slot name="header">

            </slot>
          </div>

          <div class="modal-body">
            <slot name="body">

            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">

            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</script>


<script>
    Vue.options.delimiters = ['${', '}'];
    axios.defaults.baseURL = 'http://127.0.0.1';

    var config = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    };

    var data = {
        vs_count: 1,
        input_vip: '',
        matched_dev: '',
        input_service_name: '',
        virtual_port_list: [{'virtual_port': '', 'real_count': '', 'real_server_ip': '', 'real_server_port': '', 'real_server_lb_mode': '', 'real_server_monitor':'' , 'sticky': '', 'dsr': '', 'ssl': ''}],
        writable: false,
        display_seen : false,
        confirm_btn_seen: false,
        create_btn_seen: false,
        showModal: false,
        input_rip : '',
        vs_list : ''
    }

    Vue.component('modal', {
        template: '#modal-template'
    })


    Vue.component('lb-table-box', {
        props: ['vs_list'],
        data: function() {
            return {
                checkedNames: []
            }
        },
        methods: {
            set_color: function(state) {
                if (state == 'down'){
                    return 'red';
                }
                else if(state == 'up'){
                    return 'green';
                }
            }
        },
        template:
            '<tbody>' +
            '<tr v-for="(value, key, index) in vs_list">' +
            '<td>' +
            //'${ this.vs_list[Object.keys(vs)[index]]["name"] }' +
            '${ value.name }' +
            '</td>' +
            '<td>' +
            '${ key.split(":")[0].split("/")[2] }' +
            '</td>' +
            '<td>' +
            '${ key.split(":")[1] }' +
            '</td>' +
            '<td>' +
            '${ value.pool_name.split("/")[2] }' +
            '</td>' +
            '<td>' +
            '<p v-for="(mem_value, mem_key, mem_index) in value.members">' +
            '<span v-bind:style="{ color: set_color(mem_value.state)}">' +
            '${ mem_key.split("/")[2] }' + ' ' +
            '[${ mem_value.state }]' +
            '</span>' +
            '</p>' +
            '</td>' +
            '<td>' +
            '${ value.loadBalancingMode }' +
            '</td>' +
            '<td>' +
            '${ value.Persist }' +
            '</td>' +
            '<td>' +
            '개발 예정' +
            '</td>' +
            '<td>' +
            '${ value.monitor.split("/")[2] }' +
            '</td>' +
            '<td>' +
            '<input type="checkbox" v-bind:id="`${ key.split(\':\')[0].split(\'/\')[2] }`" v-bind:value="`${ key.split(\':\')[0].split(\'/\')[2] }`" v-model="checkedNames">' +
            '</td>' +
            '</tr>' +
            '</tbody>'
    })

    var assign_vip = new Vue({
        el: '#assign_vip',
        data: data,
        methods: {
            assign: function (event) {
                axios.get('/verify_vip', {
                    params: {
                        ip: this.input_vip
                    }
                })
                .then(function (response) {
                    alert(response.data.data);
                    if (response.data.status == "200"){
                        virtual_server.writable_true();
                    }
                    else{
                        virtual_server.writable_false();
                    }
                })
                .catch(function (error) {
                    alert(error);
                });

                axios.get('/l4map', {
                    params: {
                        ip: this.input_vip
                    }
                })
                .then(function (response) {
                    assign_vip.set_matched_dev(response.data);
                })
                .catch(function (error) {
                    alert(error);
                });
            },
            set_matched_dev: function(arg){
                this.matched_dev = arg;
            },
            click_search_btn : function(){
                var self = this;
                axios.get('/search_l4check', {
                    params: {
                        ip: this.input_rip
                    }
                })
                .then(function (response) {
                    if (response.data.status == "200"){
                        console.log(response.data.data);
                        self.vs_list = response.data.data;
                    }
                    else{
                        console.log(response.data.data);
                        self.vs_list = {};
                    }
                })
                .catch(function (error) {
                    alert(error);
                });
            },
            set_vip: function(){
                this.showModal = false;
                this.input_vip = this.$children[0].$children[0].checkedNames[0];
            }
        }
    })

    Vue.component('virtual-server-box', {
        data: function() {
            return {
                vs_box_count: this.$parent.vs_count,
                virtual_port: '',
                real_count: 1,
                real_server_ip: '',
                sticky: 'No',
                dsr: 'No',
                ssl: 'No',
                real_server_port: '',
                real_server_lb_mode: 'Round Robin',
                real_server_monitor: 'No',
                writable: this.$parent.writable
            }
        },
        methods: {
            changed: function (){
                // passing to parent
                this.$parent.virtual_port_list[this.vs_box_count-1]['virtual_port'] = this.virtual_port;
                this.$parent.virtual_port_list[this.vs_box_count-1]['real_count'] = this.real_count;
                this.$parent.virtual_port_list[this.vs_box_count-1]['sticky'] = this.sticky;
                this.$parent.virtual_port_list[this.vs_box_count-1]['dsr'] = this.dsr;
                this.$parent.virtual_port_list[this.vs_box_count-1]['ssl'] = this.ssl;
                this.$parent.virtual_port_list[this.vs_box_count-1]['real_server_port'] = this.real_server_port;
                this.$parent.virtual_port_list[this.vs_box_count-1]['real_server_lb_mode'] = this.real_server_lb_mode;
                this.$parent.virtual_port_list[this.vs_box_count-1]['real_server_monitor'] = this.real_server_monitor;
                this.$parent.virtual_port_list[this.vs_box_count-1]['real_server_ip'] = this.real_server_ip;
            },
            ssl_upload: function (){
                alert("SSL 인증서 업로드 구현 예정");
            },
            delete_click: function (){
                this.$emit('delete-vs');
            }
        },
        template: '<div class="col-md-round-box">' +
        '<div class="col-md-4"> ' +
        '<div class="col-md-12"><label class="label-title">Virtual Port</label>  <button v-on:click="delete_click" class="btn btn-xs btn-danger">x</button></div> ' +
        '<div class="col-md-round-box">' +
        '<div class="col-md-12-inner" >' +
        '<label class="label-subtitle">Port</label> ' +
        '<input :disabled="writable == false" type="text" placeholder="ex. 80" required="" class="form-control input-lg" v-model="virtual_port" v-on:change="changed">' +
        '</div> ' +
        '<div class="col-md-12-inner">' +
        '<label class="label-subtitle">Sticky 사용 여부</label><select :disabled="writable == false" v-model="sticky" v-on:change="changed" class="form-control input-md"> ' +
        '<option>No</option><option>300초</option> <option>600초</option> <option>900초</option> <option>1800초</option> ' +
        '</select>' +
        '</div>' +
        '<div class="col-md-12-inner"><label class="label-subtitle">DSR 사용 여부</label> ' +
        '<select :disabled="writable == false" v-model="dsr" v-on:change="changed" class="form-control input-md"> <option>No</option> <option>Yes</option> </select>' +
        '</div> ' +
        '<div class="col-md-12-inner">' +
        '<label class="label-subtitle">SSL 인증서 사용 여부 </label><br>' +
        '<input :disabled="writable == false" v-on:change="changed" type="radio" id="ssl_yes" value="Yes" v-model="ssl" /> ' +
        '<label for="ssl_yes">Yes</label> ' +
        '<input :disabled="writable == false" v-on:change="changed" type="radio" id="ssl_no" value="No" v-model="ssl" /> ' +
        '<label for="ssl_no">No</label> ' +
        '<button v-on:click="ssl_upload" class="btn btn-sm btn-info" :disabled="ssl != \'Yes\'">SSL 인증서 업로드</button>' +
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
        '<label class="label-subtitle">Port</label><input :disabled="writable == false" type="text" v-model="real_server_port" v-on:change="changed" placeholder="ex. 80" required="" class="form-control input-md"> ' +
        '</div>' +
        '<div class="col-md-5">' +
        '<label class="label-subtitle">LB mode</label>' +
        '<select :disabled="writable == false" v-model="real_server_lb_mode" v-on:change="changed"  class="form-control input-md" > ' +
        '<option>Round Robin</option> <option>Least Connections</option> </select>' +
        '</div> ' +
        '<div class="col-md-5">' +
        '<label  class="label-subtitle">Monitor</label>' +
        '<select :disabled="writable == false" v-model="real_server_monitor" v-on:change="changed"  class="form-control input-md" > ' +
        '<option>No</option><option>http_healthcheck.jsp_skphok</option> <option>tcp</option> <option>tcp_half_open</option> <option>icmp</option> ' +
        '<option>udp</option> </select>' +
        '</div>' +
        '</div>' +
        '<div class="col-md-12">' +
        '<label class="label-subtitle">Real IP</label> ' +
        '<textarea :disabled="writable == false" v-model="real_server_ip" v-on:change="changed" name="content"  placeholder="ex. 10.10.10.10" required="" class="form-control input-md" cols="40" rows="4" >' +
        '</textarea>' +
        '<p style="color: #d43f3a;"> <br> **  Real IP 작성 방법 <br> 단일 IP : x.x.x.x,[space] (space를 넣어야 자동 줄바꿈) <br> 연속 IP : x.x.x.1~10 <br> comma로 구분하여 IP 입력할 경우 Virtual Server와 자동 매칭하여 L4를 생성함</p>' +
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
                    this.virtual_port_list.push({'virtual_port': '', 'real_count': '', 'real_server_ip': '', 'real_server_port': '', 'real_server_lb_mode': '', 'real_server_monitor':'' , 'sticky': '', 'dsr': '', 'ssl': ''});
                }
            },
            delete_this_vs: function(index) {
                this.virtual_port_list.splice(index, 1);
                this.vs_count -= 1;
                for(var idx in this.virtual_port_list){
                    for(var el in this.virtual_port_list[idx]){
                        this.$children[idx][el] = this.virtual_port_list[idx][el];
                    }
                }
            },
            writable_true: function(){
                this.writable = true;
                for(var idx in this.virtual_port_list){
                    this.$children[idx].writable = true;
                }
                this.confirm_btn_seen = true;
            },
            writable_false: function(){
                this.writable = false;
                for(var idx in this.virtual_port_list){
                    this.$children[idx].writable = false;
                }
                this.matched_dev = '';
                this.display_seen = false;
                this.confirm_btn_seen = false;
                this.create_btn_seen = false;
            }
        }
    })

    Vue.component('display-config', {
        template: '<div> matched_dev : ${ this.$parent.matched_dev }, <br> v_${ this.$parent.input_vip }_${ this.$parent.input_service_name } : ${ this.$parent.virtual_port_list }</div>'
    })

    var display_config = new Vue({
        el: '#display_config',
        data: data,
        methods: {
            click_display: function (event) {
                this.display_seen = true;
                for (var i=0; i<this.vs_count; i++) {
                    var ip_set = this.virtual_port_list[i]['real_server_ip'];
                    if(typeof(ip_set) == "string") {
                        var ip_list = ip_set.split(",");
                        var return_ip_list = [];
                        for (var ip in ip_list) {
                            if (ip_list[ip].split("~").length > 1) {
                                var prefix_ip = ip_list[ip].split("~")[0].split(".")[0] + "." + ip_list[ip].split("~")[0].split(".")[1] + "." + ip_list[ip].split("~")[0].split(".")[2] + ".";
                                if ((ip_list[ip].split("~")[1] - ip_list[ip].split("~")[0].split(".")[3]) < 1){
                                    alert(ip_list[ip] + "은 올바르지 않은 IP 대역입니다. 확인 바랍니다.");
                                    break;
                                }
                                for (var j = 0; j < ip_list[ip].split("~")[1] - ip_list[ip].split("~")[0].split(".")[3] + 1; j++) {
                                    return_ip_list.push((prefix_ip + String(Number(ip_list[ip].split("~")[0].split(".")[3]) + Number(j))).trim());
                                }
                            }
                            else {
                                return_ip_list.push(ip_list[ip].trim());
                            }
                        }
                        console.log(return_ip_list);
                        this.virtual_port_list[i]['real_server_ip'] = return_ip_list;
                        this.virtual_port_list[i]['real_count'] = return_ip_list.length;
                    }
                }

//                axios.get('/l4map', {
//                    params: {
//                        ip: this.input_vip
//                    }
//                })
//                .then(function (response) {
//                    //console.log(response.data);
//                    //alert(response.data);
//                })
//                .catch(function (error) {
//                    alert(error);
//                });
                this.create_btn_seen = true;

            }
        },
        created: function(){
            //this.data['seen'] = false;
        }
    })
</script>

{% endblock %}
