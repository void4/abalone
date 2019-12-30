<template>
    <div>
        New Game

        <b-button id="newgame" v-on:click="startGame('pvp')">PvP</b-button>

        <b-form-checkbox id="ranked" type="checkbox" v-model="ranked">Ranked?</b-form-checkbox>
        <br>
        Player name:
        <b-form-input id="invitelink" type="text" v-model="invitelink" placeholder="Enter player name"></b-form-input>
        <b-button id="copylink">Copy link</b-button>

        <b-button id="newgame2" @click="startGame('ai')">against AI</b-button>
        <b-button id="newgame3" @click="startGame('myself')">against myself</b-button>
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
      const path = `${window.location.protocol}//${window.location.hostname}:5000/newgame`;
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
  },
  mounted() {
  },
};

</script>
