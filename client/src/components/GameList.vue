<template>
    <div class="gamelist">
        Game List

        <button id="reload" v-on:click="loadgames()">Reload</button>

        <p>{{ info }}</p>
        <ul id="example-1">
          <li v-for="game in games">
            Game #{{ game.gid }}
            <div v-if="game.opponent">vs {{ game.opponent }}</div>
            <div v-else>spectating</div>
            Ranked: {{ game.ranked }}
            <div v-if="game.invited">
              <button @click="inviteresponse(game.gid, true)">Accept invitation</button>
              <button @click="inviteresponse(game.gid, false)">Reject invitation</button>
            </div>
            <div v-else>
              <div v-if="game.accepted">
                <button @click="loadgame(game.gid)">open</button>
              </div>
              <div v-else>
                Not yet accepted
              </div>
            </div>
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
      const path = `http://${window.location.hostname}:5000/gamelist`;
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
    inviteresponse(gid, accepted) {
    const path = `http://${window.location.hostname}:5000/inviteresponse`;
    axios.get(path, {params: {gid, accepted}})
      .then((res) => {
        this.loadgames();
        if (accepted) {
          this.loadgame(gid)
        }
      })
      .catch(() => {
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
    // setInterval(this.loadgames, 10000);
  },
};

</script>
