<template>
    <div>
        New Game

        <button id="newgame" v-on:click="startGame('pvp')">PvP</button>
        Ranked?<input id="ranked" type="checkbox" v-model="ranked"></button>
        <br>
        Player name:
        <input id="invitelink" type="text" v-model="invitelink">
        <button id="copylink">Copy link</button>

        <button id="newgame2" @click="startGame('ai')">against AI</button>
        <button id="newgame3" @click="startGame('myself')">against myself</button>
        <br>
        Player list:
        <ul id="example-1">
          <li v-for="player in players">
            {{ player }}
          </li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios';


export default {
  name: 'NewGame',
  data() {
    return {
      info: 'Your move',
      ranked: true,
      invitelink: '',
      players: [],
    };
  },
  components: {
  },
  methods: {
    startGame(gamemode) {
      const path = `http://${window.location.hostname}:5000/newgame`;
      axios.get(path, { params: { gamemode, ranked: this.ranked, invite: this.invitelink } })
        .then((res) => {
          this.invitelink = res.data.invitelink;
          this.$root.$emit('loadgames');
          this.$root.$emit('loadgame', res.data.gid);
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
    getPlayers() {
      const path = `http://${window.location.hostname}:5000/players`;
      axios.get(path)
        .then((res) => {
          this.players = res.data.players;
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
  },
  mounted() {
    this.getPlayers();
  },
};

</script>
