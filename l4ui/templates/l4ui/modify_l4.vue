{% extends 'l4ui/base.html' %}
{% block content %}
<div class="container">
    <div class="row home-intro text-center">

        <h2 class="tagline">L4 변경/삭제</h2>
        <hr class="small">


        <div id="lb_table">
            <label>Virtual IP 또는 Real IP를 입력하세요 : </label>
            <input v-model="input_ip" type="text"/>
            <input id="search_btn" type="button" class="btn btn-info" value="조회" v-on:click="click_search_btn"/>

            <br><br>

            <div class="row">
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
                                <th>작업</th>
                            </tr>
                            </thead>
                            <tbody is="lb-table-box" v-bind:vs_list="vs_list">
                            </tbody>
                        </table>
                </div>
            </div>
        </div>

    </div>
</div>


<script src="/static/js/jquery/1.11.3/jquery.min.js"></script>
<script src="/static/js/jquery.redirect.js"></script>
<link href="/static/css/l4style.css" rel="stylesheet" type="text/css">
<script src="/static/js/vue.js"></script>
<script src="/static/js/axios.min.js"></script>

<script>
    Vue.options.delimiters = ['${', '}'];
    axios.defaults.baseURL = 'http://127.0.0.1';

    Vue.component('lb-table-box', {
        props: ['vs_list'],
        data: function() {
            return {
                classObject: {
                    color: 'red'
                }
            }
        },
//        methods: {
//
//        },
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
        '<div v-for="(mem_value, mem_key, mem_index) in value.members">' +
        '${ mem_key.split("/")[2] }' + ' ' +
        '<span v-bind:style="classObject">' +
        '[${ mem_value.state }]' +
        '</span>' +
        '</div>' +
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
        '<button v-if="" class="btn btn-success" v-on:click="">변경</button>'+
        '<button v-if="" class="btn btn-danger" v-on:click="">삭제</button>'+
        '</tr>' +
        '</tbody>'
    })

    var lb_table = new Vue({
        el: '#lb_table',
        data: {
            input_ip : '',
            vs_list : ''
        },
        methods: {
            click_search_btn : function(){
                var self = this;
                axios.get('/search_l4check', {
                    params: {
                        ip: this.input_ip
                    }
                })
                .then(function (response) {
                    if (response.data.status == "200"){
                        console.log(response.data.data);
                        self.vs_list = response.data.data;
                    }
                })
                .catch(function (error) {
                    alert(error);
                });
            }
        }
    })


</script>

{% endblock %}
