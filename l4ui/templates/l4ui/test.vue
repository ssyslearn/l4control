<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <script src="https://unpkg.com/vue"></script>
    <title>JS Bin</title>
</head>
<body>

<div id="app">
    <p v-text="message"></p>
</div>

<div id="app2">
    <p v-text="message2"></p>
</div>


<div id="vue-instance">
    <input v-model='items'/>
    <span v-for="item in items">
        ${ item }
    </span>
</div>

<div id="another-instance">
    <span v-for="item in items">
        ${ item }
    </span>
</div>


<!-- 백업 !!! -->

<!--
<div id="virtual_server_box" class="col-md-round-box">
              <div id="assign_vport" class="col-md-4">
              <div class="col-md-12">
              <label class="label-title" id="label_virtual_port">Virtual Port</label>
          </div>
          <div class="col-md-round-box">
          <div class="col-md-12-inner">
          <label class="label-subtitle">Port</label>
          <input v-model="input_vport" type="text" id="rip" placeholder="ex. 80" required="" class="form-control input-lg">
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

      -->


<script>

    Vue.options.delimiters = ['${', '}'];

    var data = {
        items: []
    }

    var app = new Vue({
        el: '#app',
        data: {
            message: '안녕하세요 Vue!'
        }
    })

    var app2 = new Vue({
        el: '#app2',
        data: {
            message2: '안녕하세요 Vue2!'
        }
    })

    var vm = new Vue({
        el: '#vue-instance',
        data: data
    })

    var vm2 = new Vue({
        el: '#another-instance',
        data: data
    })

</script>
</body>
</html>