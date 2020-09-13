<template>
    <div>
        <h3>{{ $t('chat') }}</h3>
        <br>
        <textarea id="chatarea" type="text" v-model="chat"/>
        <br>
        <input id="chatinput" type="text" v-model="chatinput">
        <button id="chatsubmit" @click="chatsubmit()">{{ $t('submit') }}</button>
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
      const path =`${window.location.protocol}//${window.location.hostname}:10000/abasocket/chat`;
      axios.get(path, { params: { chatinput: this.chatinput } })
        .then((res) => {
          //this.chat += res.data.chat;
          this.chatinput = "";
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
  },
  mounted() {
    this.$root.$on('chatappend', (msg) => {
      this.chat += msg + "\n";
      var chatarea = document.getElementById("chatarea");
      chatarea.scrollTop = chatarea.scrollHeight;
    });

    // Get the input field
    var input = document.getElementById("chatinput");

    // Execute a function when the user releases a key on the keyboard
    let vm = this;
    input.addEventListener("keydown", function(event) {
      // Number 13 is the "Enter" key on the keyboard
      if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        vm.chatsubmit();
      }
    });
  },
};

</script>
