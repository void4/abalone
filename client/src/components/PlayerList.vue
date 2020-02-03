<template>
  <div class="playerlist">
    <h3>{{ $t('playerlist') }}</h3>
    <b-list-group>
      <b-list-group-item v-for="player in players">
        <b title="Abalone Master" class="titles">{{player.titles}}</b>
        {{ player.name }}
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<style scoped>
* {
  background-color: rgba(100, 100, 100, 0.1);
}

.titles {
    color: #d59020;
}
</style>


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
      const path = `${window.location.protocol}//${window.location.hostname}:5000/players`;
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
