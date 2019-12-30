import Vue from 'vue';
import VueRouter from 'vue-router';
import About from '../components/About.vue';
import Play from '../components/Play.vue';
import Stats from '../components/Stats.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/about',
    name: 'About',
    component: About,
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
