<template>
  <div>
    <router-view/>
    <chat-example/>
  </div>
</template>

<script>
import ChatExample from './components/ChatExample.vue'

export default {
  name: 'App',
  components: { ChatExample }
}
</script>
