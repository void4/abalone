import Vue from 'vue';
import App from './App.vue';
import router from './router';

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import VueI18n from 'vue-i18n'

Vue.use(BootstrapVue)
Vue.use(VueI18n)

var i18n = new VueI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en: {
      hello: 'Hello',
      play: 'Play',
      stats: 'Stats',
      about: 'About',
      tut0: '1,2 or 3 marbles can be moved.',
      tut1: 'The objective of the game is to push 6 marbles of the opponent off the board.',
      tut2: 'To move the opponents\' marbles, you always need to push with one more - 3 own can push 2 or 1 marbles, 2 can push 1 marble of the opponent.',
      tut3: 'To move marbles in the direction of a line, select the last one and then the field on which they are moved.',
      tut4: 'To move marbles sideways, select all of them and then, the field in which direction they should be moved - relative to the last selected marble.',
      quote: 'Quote of the day:',
      standard: 'Standard',
      germandaisy: 'German Daisy',
      belgiandaisy: 'Belgian Daisy',
      unlimited: 'Unlimited',
      min5: '5 Minutes',
      min15: '15 Minutes',
      pvp: 'Player vs Player',
      ranked: 'Ranked?',
      playername: 'Player name',
      enterplayername: 'Enter player name',
      copylink: 'Copy Link',
      againstai: 'Against AI',
      againstmyself: 'Against Myself',
      gamelist: 'Gamelist',
      reload: 'Reload',
      playerlist: 'Player list',
      surrender: 'Surrender',
      leave: 'Leave',
      failedloadinggames: 'Failed to load games. Are you logged in?',
      newgame: 'New Game',

    },
    de: {
      hello: 'Hallo',
      play: 'Spielen',
      stats: 'Statistiken',
      about: 'Info',
      tut0: 'Es können 1,2 oder 3 Kugeln geschoben werden.',
      tut1: 'Ziel des Spiels ist es 6 Kugeln des Gegners aus dem Spielfeld zu schieben.',
      tut2: 'Um gegnerische Kugeln zu verschieben, benötigt man immer eine mehr, 3 eigene können 2 oder 1 Kugel des Gegners schieben, 2 eine.',
      tut3: 'Zum Verschieben von Kugeln in einer Reihe: erst die hinterste Kugel auswählen und dann die Kugel/das Feld auf das geschoben werden soll.',
      tut4: 'Beim seitlichen Verschieben: Alle Kugeln die verschoben werden sollen auswählen und dann das Feld in dessen Richtung von der letzten Kugel aus verschoben werden soll.',
      quote: 'Zitat des Tages:',
      standard: 'Standard',
      germandaisy: 'German Daisy',
      belgiandaisy: 'Belgian Daisy',
      unlimited: 'Unbegrenzt',
      min5: '5 Minuten',
      min15: '15 Minuten',
      pvp: 'Spieler gegen Spieler',
      ranked: 'Gewertet?',
      playername: 'Spielername',
      enterplayername: 'Spielername eingeben',
      copylink: 'Link kopieren',
      againstai: 'Gegen KI',
      againstmyself: 'Gegen mich selbst',
      gamelist: 'Spieleliste',
      reload: 'Neu laden',
      playerlist: 'Spielerliste',
      surrender: 'Aufgeben',
      leave: 'Verlassen',
      failedloadinggames: 'Spieleliste konnte nicht geladen werden. Bist Du eingeloggt?',
      newgame: 'Neues Spiel',
    }
  }
})

Vue.config.productionTip = false;

new Vue({
  router,
  i18n,
  render: h => h(App),
}).$mount('#app');
