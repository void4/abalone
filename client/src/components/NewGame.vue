<template>
    <div>
        New Game

        <button id="newgame" v-on:click="startGame('pvp')">PvP</button>
        Ranked?<input id="ranked" type="checkbox" v-model="ranked"></button>
        <input id="invitelink" type="text" v-model="invitelink">
        <button id="copylink">Copy link</button>

        <button id="newgame2" @click="startGame('ai')">against AI</button>
        <button id="newgame3" @click="startGame('myself')">against myself</button>
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
    };
  },
  components: {
  },
  methods: {
    startGame(gamemode) {
      const path = 'http://localhost:5000/newgame';
      axios.get(path, { params: { gamemode, ranked: this.ranked } })
        .then((res) => {
          this.invitelink = res.data.invitelink;
          this.$root.$emit('loadgames');
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
  },
  created() {
  },
};

</script>
