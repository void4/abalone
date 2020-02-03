<template>
  <div id="app">
    <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
    <div>
      <b-nav tabs align="center">
      <b-nav-item to="/">{{ $t('play') }}</b-nav-item>
      <b-nav-item to="/rules">{{ $t('rules') }}</b-nav-item>
      <b-nav-item v-if="showstats" to="/stats">{{ $t('stats') }}</b-nav-item>
      <b-nav-item to="/about">{{ $t('about') }}</b-nav-item>
      <b-nav-item to="/settings">{{ $t('settings') }}</b-nav-item>
      </b-nav>
    </div>
    <router-view/>
  </div>
</template>

<style>

html {
  background-color: #edebe9;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #edebe9;
}

#nav {
  padding: 30px;
  background-color: #edebe9;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}



*, ::after, ::before {
    box-sizing: border-box;
    outline: none !important;
    border: none !important;
    -webkit-box-shadow: none !important;
    box-shadow: none !important;
}
</style>

<script>

export default {
  name: 'App',
  data() {
    return {
      showstats: true,
    };
  },
  mounted() {
    this.$root.$on('showstats', () => {
      this.showstats = true;
    });
  },
};

</script>
