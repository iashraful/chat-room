<template>
  <div>
    <h1>Chat</h1>
    <input v-model="msg"/>
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script>
export default {
  name: 'ChatExample',
  data () {
    return {
      msg: '',
      connection: null
    }
  },
  mounted () {
    this.connection = new WebSocket('ws://localhost:8083/ws/')
    this.connection.onmessage = (event) => {
      console.log(event)
    }
  },
  methods: {
    sendMessage () {
      console.log(this.msg)
      this.connection.send(JSON.stringify({ msg: this.msg }))
    }
  }

}
</script>
