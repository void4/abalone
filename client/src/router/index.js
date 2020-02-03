import Vue from 'vue';
import VueRouter from 'vue-router';
import Play from '../components/Play.vue';
import Tutorial from '../components/Tutorial.vue';
import Stats from '../components/Stats.vue';
import About from '../components/About.vue';
import Settings from '../components/Settings.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Play',
    component: Play,
  },
  {
    path: '/rules',
    name: 'Tutorial',
    component: Tutorial,
  },
  {
    path: '/stats',
    name: 'Stats',
    component: Stats,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
