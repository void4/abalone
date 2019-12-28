<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import cookie from 'cookie-machine';

import HelloWorld from '@/components/HelloWorld.vue';

axios.interceptors.request.use((config) => {
  const token = cookie.get('access_token');

  if (token != null) {
    /* eslint-disable no-param-reassign */
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
}, err => Promise.reject(err));


export default {
  name: 'home',
  components: {
    HelloWorld,
  },
};
</script>
