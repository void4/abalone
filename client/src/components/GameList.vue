<template>
    <div class="gamelist">
        <h3>{{ $t('gamelist') }}</h3>

        <button id="reload" v-on:click="loadgames()">⟳ {{ $t('reload') }}</button>

        <p>{{ info }}</p>
        <b-list-group>
          <b-list-group-item v-for="game in games">
            Game #{{ game.gid }}
            <div v-if="game.opponent">{{ $t('vs') }} {{ game.opponent }}</div>
            <div v-else>spectating</div>
            {{ $t(game.ranked ? 'ranked' : 'unranked') }}
            <br>
            <template v-if="game.invited">
              <button @click="inviteresponse(game.gid, true)">{{ $t('acceptinvite') }}</button>
              <button @click="inviteresponse(game.gid, false)">{{ $t('rejectinvite') }}</button>
            </template>
            <template v-else>
              <template v-if="game.accepted">
                <button @click="loadgame(game.gid)">{{ $t('open') }}</button>
              </template>
              <template v-else>
                Not yet accepted
              </template>
            </template>
          </b-list-group-item>
        </b-list-group>
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
      console.log("LOADGAMES")
      const path = `${window.location.protocol}//${window.location.hostname}/abasocket/gamelist`;
      axios.get(path)
        .then((res) => {
          //console.log(res.data);
          this.info = res.data.info;
          var firstload = this.games.length == 0;
          this.games = res.data.games;
          if (firstload) {
            //console.log("FIRSTLOAD")
            this.loadgame(this.games[0].gid);
          }
        })
        .catch(() => {
          this.games = [];
          this.info = this.$t('failedloadinggames');
        });
    },
    inviteresponse(gid, accepted) {
    const path = `${window.location.protocol}//${window.location.hostname}/abasocket/inviteresponse`;
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
