import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../components/Home.vue';
import Play from '../components/Play.vue';
import Stats from '../components/Stats.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/about',
    name: 'home',
    component: Home,
  },
  {
    path: '/',
    name: 'Play',
    component: Play,
  },
  {
    path: '/stats',
    name: 'Stats',
    component: Stats,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
