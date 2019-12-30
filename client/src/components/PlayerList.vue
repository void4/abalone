<template>
  <div class="playerlist">
  Player list:
  <b-list-group>
    <b-list-group-item v-for="player in players">
      {{ player }}
    </b-list-group-item>
  </b-list-group>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'PlayerList',
  data() {
    return {
      players: [],
    };
  },
  components: {
  },
  methods: {
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
