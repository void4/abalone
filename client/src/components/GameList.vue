<template>
    <div class="gamelist">
        Game List

        <button id="reload" v-on:click="loadgames()">Reload</button>

        <p>{{ info }}</p>
        <ul id="example-1">
          <li v-for="game in games">
            <button @click="loadgame(game.id)">Switch to Game #{{ game.id }}</button>
          </li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios';


export default {
  name: 'GameList',
  data() {
    return {
      info: '-',
      username: 'test',
      games: [],
    };
  },
  components: {
  },
  methods: {
    loadgames() {
      const path = 'http://localhost:5000/gamelist';
      axios.get(path)
        .then((res) => {
          console.log(res.data);
          this.info = res.data.info;
          this.games = res.data.games;
        })
        .catch(() => {
          this.games = [];
          this.info = 'Failed to load games. Are you logged in?';
        });
    },

    loadgame(gid) {
      this.$root.$emit('loadgame', gid);
    },
  },
  created() {
    this.loadgames();
  },
  mounted() {
    this.$root.$on('loadgames', () => {
      this.loadgames();
    });
  },
};

</script>
