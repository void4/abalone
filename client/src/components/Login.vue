<template>
    <div>
        <h3>Login</h3>

        <div v-if="!loggedin">
          Username:<input id="username" type="text" v-model="username">
          Password:<input id="password" type="password" v-model="password">
          <button id="login" v-on:click="login()">Login</button>
          <button id="register" v-on:click="register()">Register</button>
        </div>

        <div v-if="loggedin">
          <button id="logout" v-on:click="logout()">Logout</button>
        </div>
        <p>{{ info }}</p>
    </div>
</template>

<script>
import axios from 'axios';
import cookie from 'cookie-machine';


export default {
  name: 'Login',
  data() {
    return {
      info: '-',
      username: '',
      password: '',
      token: '',
      loggedin: false,
    };
  },
  components: {
  },
  methods: {
    register() {
      const path = 'http://localhost:5000/register';
      axios.get(path, { params: { username: this.username, password: this.password } })
        .then((res) => {
          this.info = res.data.info;
          if (res.data.status === 'success') {
            this.login();
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
    login() {
      const path = 'http://localhost:5000/login';
      axios.get(path, { params: { username: this.username, password: this.password } })
        .then((res) => {
          this.info = res.data.info;
          if (res.data.status === 'success') {
            this.loggedin = true;
            this.password = '';
            this.token = res.data.token;
            cookie.set('access_token', this.token);
            this.$root.$emit('loadgames');
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
    logout() {
      // delete cookie
      cookie.set('access_token', '');
      this.loggedin = false;
      // clear game list
      this.$root.$emit('loadgames');
    },
    auth() {
      const path = 'http://localhost:5000/auth';
      axios.get(path, { params: {} })
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  mounted() {
    // check if logged in, if yes, loggedin = true
    this.loggedin = cookie.get('access_token').length > 0;
  },
};

</script>
