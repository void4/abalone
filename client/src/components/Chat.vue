<template>
    <div>
        <h3>Chatto</h3>
        <br>
        <textarea id="chatarea" type="text" v-model="chat"/>
        <br>
        <input id="chatinput" type="text" v-model="chatinput">
        <button id="chatsubmit" @click="chatsubmit()">Submit</button>
        {{ info }}
    </div>
</template>

<style scoped>
#chatarea {
  width: 90%;
}
</style>

<script>
import axios from 'axios';


export default {
  name: 'Chat',
  data() {
    return {
      chatinput: '',
      chat: '',
      info: 'Joined chat',
    };
  },
  components: {
  },
  methods: {
    chatsubmit() {
      const path = 'http://localhost:5000/chat';
      axios.get(path, { params: { chatinput: this.chatinput } })
        .then((res) => {
          this.chat += res.data.chat;
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
  },
  mounted() {
  
  },
};

</script>
