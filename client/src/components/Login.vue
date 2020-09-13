<template>
    <div>
        <h3>Login</h3>

        <div v-if="!loggedin">
          <b-form action="javascript:void(0);">
            {{ $t('username') }}<b-form-input id="username" type="text" v-model="username"></b-form-input>
            {{ $t('password') }}<b-form-input id="password" type="password" v-model="password"></b-form-input>
            <b-button id="login" v-on:click="login()">{{ $t('login') }}</b-button>
            <button id="register" v-on:click="register()">{{ $t('register') }}</button>
          </b-form>
        </div>

        <div v-if="loggedin">
          <b-button id="logout" v-on:click="logout()">{{ $t('logout') }}</b-button>
        </div>
        <p>{{ info }}</p>
    </div>
</template>

<script>
import axios from 'axios';
import cookie from 'cookie-machine';

axios.interceptors.request.use((config) => {

  if (config.params !== undefined) {
    const tmpid = cookie.get('tmpid');
    config.params["tmpid"] = tmpid;
  }

  const token = cookie.get('access_token');

  if (token != null) {
    /* eslint-disable no-param-reassign */
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
}, err => Promise.reject(err));

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
      const path = `${window.location.protocol}//${window.location.hostname}:10000/abasocket/register`;
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
      const path = `${window.location.protocol}//${window.location.hostname}:10000/abasocket/login`;
      axios.get(path, { params: { username: this.username, password: this.password } })
        .then((res) => {
          this.info = res.data.info;
          if (res.data.status === 'success') {
            this.loggedin = true;
            this.password = '';
            this.token = res.data.token;
            cookie.set('access_token', this.token);
            this.$root.$emit('loadgames');
            this.$root.$emit('showstats');
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
  },
  created() {
  },
  mounted() {
    // check if logged in, if yes, loggedin = true
    this.loggedin = cookie.get('access_token').length > 0;
  },
};

</script>
