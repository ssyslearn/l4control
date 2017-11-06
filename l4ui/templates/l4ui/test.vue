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



<script>
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
</script>
</body>
</html>