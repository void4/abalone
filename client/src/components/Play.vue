<template>
    <div>
        <div class="sidebar">
        <NewGame/>
        <hr>
        <GameList/>
        <PlayerList/>
        <Settings/>
        </div>

        <div class="gamebar">
          <br>
          <template v-if="gameinfo">
            <b>{{ gameinfo.p1 }} {{ $t('vs') }} {{ gameinfo.p2 }}</b>
            <br>
            <h5 v-if="gameinfo.ranked">{{ $t('ranked') }}</h5>
            <h5 v-else>({{ $t('unranked') }})</h5>
            <h5 v-if="gameinfo.p1time || gameinfo.p2time" v-bind:class="{ p1timeover: !gameinfo.p1time || !gameinfo.p2time }">P1: {{ gameinfo.p1time }} | {{ gameinfo.timetomove }} | P2: {{ gameinfo.p2time }}</h5>
            <h5 v-if="gameinfo.out">{{ '○'.repeat(gameinfo.out[0]) }} | {{ '●'.repeat(gameinfo.out[1]) }}</h5>
          </template>
          <!--<pre style="text-align: left;">{{ game }}</pre>-->
          <canvas id="cvs"></canvas>
          <!--<button id="move" v-on:click="move()">Move</button>-->
          <p>{{ turn }}</p>
          <p>{{ info }}</p>
          <button id="surrender" v-on:click="surrender()">{{ $t('surrender') }}</button>
          <button v-if="!gameinfo.ranked" id="leave" v-on:click="leave()">{{ $t('leave') }}</button>
          <input id="moveinput" type="hidden">
        </div>

        <div class="userbar">
          <Login/>
          <hr>
          <Tutorial/>
          <hr>
          <Chat/>
        </div>
    </div>
</template>


<style>
.p1timeover {
  color: red;
}

.sidebar {
  position: absolute;
  top: 0px;
  left: 0;
  width: 18%;
  align: left;
  background-color: rgba(200,200,200,0.5);
  z-index: 100;
  overflow-y: scroll;
  bottom: 0;
}

.gamebar {
  position: absolute;
  align: center;
  left: 0px;
  width: 100%;
  background-color: #edebe9;
}

html {
  background-color: #edebe9;
}

.userbar {
  position: absolute;
  top: 0px;
  right: 0px;
  width: 18%;
  align: right;
  background-color: rgba(0,0,250,0.1);
  z-index: 100;
  bottom: 0;
}

</style>

<script>
import {Container} from 'pixi.js'
import {Renderer} from 'pixi.js'
import {Sprite} from 'pixi.js'
import {Graphics} from 'pixi.js'
import {Filter} from 'pixi.js'
import {Matrix} from 'pixi.js'
import {Texture} from 'pixi.js'
import {BaseTexture} from 'pixi.js'
import * as PIXI from 'pixi.js';
import SOUND from 'pixi-sound';

PIXI["sound"] = SOUND; // ts wont complain

import axios from 'axios';
import NewGame from '@/components/NewGame.vue';
import Login from '@/components/Login.vue';
import GameList from '@/components/GameList.vue';
import Chat from '@/components/Chat.vue';
import Tutorial from '@/components/Tutorial.vue';
import PlayerList from '@/components/PlayerList.vue';
import Settings from '@/components/Settings.vue';

function randomchoice(choices) {
  var index = Math.floor(Math.random() * choices.length);
  return choices[index];
}

export default {
  name: 'Play',
  data() {
    return {
      msg: '-',
      name: '?',
      game: '-',
      state: [],
      gameid: 0,
      info: 'Your move',
      gameinfo: {},
      sprites: [],
      selected: [],
      ranked: false,
      turn: '',
      timeref: null,
    };
  },
  components: {
    NewGame,
    Login,
    GameList,
    Chat,
    Tutorial,
    PlayerList,
    Settings,
  },
  methods: {
    startTimer() {
      console.log("STARTING TIMER")
      this.timeref = setInterval(this.timer, 1000)
      console.log(this.timer)
    },
    timer() {
      console.log("Timer")
      if (this.gameinfo.next == 0) {
        if (this.gameinfo.p1time <= 0) {

        } else {
          this.gameinfo.p1time -= 1;
        }
      } else {
        if (this.gameinfo.p2time <= 0) {

        } else {
          this.gameinfo.p2time -= 1;
        }
      }
    },
    getGame() {
      const path = `${window.location.protocol}//${window.location.hostname}:5000/game`;
      axios.get(path, { params: { id: this.gameid } })
        .then((res) => {
          this.game = res.data.board;
          this.state = res.data.state;
          this.info = res.data.info;
          //console.log("GAMEINFO", this.gameinfo)
          this.gameinfo = res.data.gameinfo;
          this.drawGame();
          if (this.timeref == null && this.gameinfo.timetomove && this.gameinfo.p1time < this.gameinfo.timetomove) {
            this.startTimer();
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
    move() {
      const movetext = document.getElementById('moveinput').value;

      const path = `${window.location.protocol}//${window.location.hostname}:5000/game`;
      axios.get(path, { params: { id: this.gameid, move: movetext } })
        .then((res) => {
          this.game = res.data.board;
          this.state = res.data.state;
          this.info = res.data.info;
          this.gameinfo = res.data.gameinfo;
          this.selected = [];
          this.drawGame();
          if (this.timeref == null && this.gameinfo.timetomove && this.gameinfo.p1time < this.gameinfo.timetomove) {
            this.startTimer();
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
    leave() {
      document.getElementById('moveinput').value = "leave";
      this.move();
    },
    surrender() {
      document.getElementById('moveinput').value = "surrender";
      this.move();
    },
    initGame() {
      let cvs = document.getElementById('cvs')
      cvs.width = 512
      cvs.height = 512
      let renderer = new Renderer({width: cvs.width, height: cvs.height, backgroundColor : 0xedebe9, view: cvs, antialias: true} )
      this.renderer = renderer
      let container = new Container()
      this.container = container;

      //console.log(PIXI)
      this.sounds = [];
      for (let i=0;i<1;i++) {
        this.sounds.push(PIXI.sound.Sound.from("move"+i+'.mp3'));
      }

      this.tex_board = Texture.from("board.svg")
      let sprite = new Sprite(this.tex_board)
      sprite.x = 0;
      sprite.y = 0;
      sprite.width = 512;
      sprite.height = 512;
      container.addChild(sprite)

      let img = new Image()
      img.src = 'field.png';
      let vm = this;

      function onDown(evt) {
        //this.alpha = 0.5;
        let ball = vm.state[this.index][1];
        let selected = vm.selected.includes(this.index);
        //console.log(this.index, vm.selected, selected)
        if (!selected) {
          if (ball == null || (ball != vm.gameinfo.next)) {
            console.log("attempt move", vm.selected, this.index)
            document.getElementById('moveinput').value = JSON.stringify([vm.selected, this.index])
            vm.move();
          } else {

            if (ball == 0 && vm.gameinfo.next == 0) {
              this.texture = vm.tex_zero_s;
              vm.selected.push(this.index);
            } else if (ball == 1 && vm.gameinfo.next == 1) {
              this.texture = vm.tex_one_s;
              vm.selected.push(this.index);
            }
          }
        } else {
          vm.selected = vm.selected.filter(e => e!=this.index);
          if (ball == 0) {
            this.texture = vm.tex_zero;
          } else if (ball == 1) {
            this.texture = vm.tex_one;
          }
        }
        vm.renderer.render(vm.container)
      }

      img.onload = function() {
        const ROWS = [5,6,7,8,9,8,7,6,5];
        // eslint-disable-next-line
        let i = 0;
        // eslint-disable-next-line
        let sw = (cvs.width/11);
        let sh = (cvs.height/11)
        vm.tex_empty = new Texture(new BaseTexture(img));
        for (var y=0;y<ROWS.length;y++) {
          for (var x=0;x<ROWS[y];x++) {
            let sprite = new Sprite(vm.tex_empty)
            sprite.index = i;
            sprite.interactive = true;
            sprite.on('mousedown', onDown);
            sprite.on('touchstart', onDown);
            sprite.x = sw*x+(9-ROWS[y])*0.5*sw + sw;
            sprite.y = (sh*0.9)*y + sh*1.4;
            sprite.width = sw*0.9;
            sprite.height = sh*0.9;
            vm.sprites.push(sprite)
            container.addChild(sprite)
            i += 1;
          }
        }
        vm.tex_zero = Texture.from("field0.png")
        /*
        img.src = 'field0.png';
        img.onload = function() {
          vm.tex_zero = new Texture(new BaseTexture(img));
        }
        */
        vm.tex_one = Texture.from("field1.png")
        vm.tex_zero_s = Texture.from("field0s.png")
        vm.tex_one_s = Texture.from("field1s.png")


        renderer.render(container)
      }
    },
    drawGame() {

      var changes = 0;
      for (const [index, element] of this.state.entries()) {
        let sprite = this.sprites[index];
        let oldtexture = sprite.texture;
        if (element[1] == null) {
          sprite.texture = this.tex_empty;
          sprite.cursor = 'pointer';
        } else if (element[1] == 0) {
          sprite.texture = this.tex_zero;
          sprite.cursor = 'grab';
        } else {
          sprite.texture = this.tex_one;
          sprite.cursor = 'grab';
        }

        if (oldtexture != sprite.texture) {
          changes += 1;
        }
      }

      if (changes > 0) {
        //console.log("SOUND", this.$settings.sound)
        if (this.$settings.sound) {
          this.sounds[0].play();
        }
      }

      this.renderer.render(this.container)
      // firefox tab title has inverted colors...
      let nextball = '-'
      if (this.gameinfo.next == 0) {
          nextball = '○';
      } else {
          nextball = '●';
      }
      //console.log(nextball)
      window.document.title = "Abalone | " + nextball + " 's " + this.$t('turn');
      this.turn = nextball + " 's " + this.$t('turn');
    },
    blinkTab(message) {
      var oldTitle = document.title,                                                           /* save original title */
          timeoutId,
          blink = function() { document.title = document.title == message ? ' ' : message; },  /* function to BLINK browser tab */
          clear = function() {                                                                 /* function to set title back to original */
            clearInterval(timeoutId);
            document.title = oldTitle;
            window.onmousemove = null;
            timeoutId = null;
          };

      if (!timeoutId) {
        timeoutId = setInterval(blink, 1000);
        window.onmousemove = clear;                                                            /* stop changing title on moving the mouse */
      }
    },
  },
  created() {
    this.source = new EventSource(`${window.location.protocol}//${window.location.hostname}:5000/stream`);
    // console.log(this.source)

    this.source.onopen = function(evt) {
      // console.log("OPEN", evt)
    }

    let vm = this;
    this.source.onmessage = function (event) {
      console.log("EVT", event.data);
      vm.$root.$emit('chatappend', event.data);
      vm.getGame();
    };


    this.source.onerror = function(event) {
      console.log(event)
      if (event.eventPhase == EventSource.CLOSED) {
          this.source.close();
          console.log("Event Source Closed");
      }
    }
  },
  destroyed() {
    //console.log("Destroyed")
    this.source.close();
  },
  mounted() {

    this.initGame();

    this.getGame();

    // this.blinkTab("MOVE ALREADY YOU SLOW F*CK")


    this.$root.$on('loadgame', (gid) => {
      console.log('Load', gid);
      this.gameid = gid;
      this.getGame();
    });

  },
};

</script>
