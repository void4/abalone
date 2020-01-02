<template>
    <div>
        <h3>{{ $t('newgame') }}</h3>

          <b-form-radio-group
            id="btn-radios-1"
            v-model="layout"
            :options="options"
            buttons
            name="radios-btn-default"
          ></b-form-radio-group>
        </b-form-group>

        <b-form-radio-group
          id="btn-radios-1"
          v-model="timetomove"
          :options="timeoptions"
          buttons
          name="radios-btn-default"
        ></b-form-radio-group>
      </b-form-group>

        <b-button id="newgame" v-on:click="startGame('pvp')">{{ $t('pvp') }}</b-button>

        <b-form-checkbox id="ranked" type="checkbox" v-model="ranked">{{ $t('ranked') }}</b-form-checkbox>
        <br>
        <b-form-input id="invitelink" type="text" v-model="invitelink" :placeholder="$t('enterplayername')"></b-form-input>
        <b-button id="copylink">{{ $t('copylink') }}</b-button>

        <b-button id="newgame2" @click="startGame('ai')">{{ $t('againstai') }}</b-button>
        <b-button id="newgame3" @click="startGame('myself')">{{ $t('againstmyself') }}</b-button>
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
      layout: null,
      options: [
        { text: 'Standard', value: null },
        { text: 'German Daisy', value: '-----00--11000-111-00--11-----------11--00-111-00011--00-----' },
        { text: 'Belgian Daisy', value: '00-11000111-00-11---------------------------11-00-11100011-00' }
      ],
      timetomove: null,
      timeoptions: [
        { text: this.$t('unlimited'), value: null },
        { text: this.$t('min5'), value: 5*60 },
        { text: this.$t('min15'), value: 15*60 },
      ]
    };
  },
  components: {
  },
  methods: {
    startGame(gamemode) {
      const path = `${window.location.protocol}//${window.location.hostname}:5000/newgame`;
      axios.get(path, { params: { gamemode, ranked: this.ranked, invite: this.invitelink, timetomove: this.timetomove, layout: this.layout } })
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
