<template>
    <div>
            <p>{{ msg }}</p>
        Test :)
        <p>{{ name }}</p>

        <div class="sidebar">
        <NewGame/>
        <GameList/>
        </div>

        <div class="gamebar">
          Gameinfo: {{ gameinfo }}
          <br>
          <b>{{ gameinfo.p1 }} vs. {{ gameinfo.p2 }}</b>
          <pre style="text-align: left;">{{ game }}</pre>
          <canvas id="cvs">
          </canvas>
          <input id="moveinput" type="text">

          <button id="move" v-on:click="move()">Move</button>
          <p>{{ state }}</p>
          <p>{{ info }}</p>
          <button id="surrender" v-on:click="surrender()">Surrender</button>
        </div>

        <div class="userbar">
          <Login/>
          <Chat/>
        </div>
    </div>
</template>


<style>
.sidebar {
  position: absolute;
  top: 0px;
  width: 18%;
  align: left;
  background-color: rgba(200,200,200,0.5);
}

.gamebar {
  position: absolute;
  align: center;
  width: 100%;
  margin-left: 18%;
}

.userbar {
  position: absolute;
  top: 0px;
  right: 0px;
  width: 18%;
  align: right;
  background-color: rgba(0,0,250,0.1);
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

import axios from 'axios';
import NewGame from '@/components/NewGame.vue';
import Login from '@/components/Login.vue';
import GameList from '@/components/GameList.vue';
import Chat from '@/components/Chat.vue';

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
    };
  },
  components: {
    NewGame,
    Login,
    GameList,
    Chat,
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/ping';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
    getName() {
      const path = 'http://localhost:5000/name';
      axios.get(path)
        .then((res) => {
          this.name = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
    getGame() {
      const path = 'http://localhost:5000/game';
      axios.get(path, { params: { id: this.gameid } })
        .then((res) => {
          this.game = res.data.board;
          this.state = res.data.state;
          this.info = res.data.info;
          this.gameinfo = res.data.gameinfo;
          this.drawGame();
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
    move() {
      const movetext = document.getElementById('moveinput').value;

      const path = 'http://localhost:5000/game';
      axios.get(path, { params: { id: this.gameid, move: movetext } })
        .then((res) => {
          this.game = res.data.board;
          this.state = res.data.state;
          this.info = res.data.info;
          this.gameinfo = res.data.gameinfo;
          this.selected = [];
          this.drawGame();
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
    initGame() {
      let cvs = document.getElementById('cvs')
      cvs.width = 512
      cvs.height = 512
      let renderer = new Renderer({width: cvs.width, height: cvs.height, backgroundColor : 0xffff00, view: cvs, antialias: true} )
      this.renderer = renderer
      let container = new Container()
      this.container = container;
      let img = new Image()
      img.src = 'field.png';
      let vm = this;

      function onDown(evt) {
        //this.alpha = 0.5;
        let ball = vm.state[this.index][1];
        let selected = vm.selected.includes(this.index);
        console.log(this.index, vm.selected, selected)
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
        let sw = (cvs.width/10);
        let sh = (cvs.height/10)
        vm.tex_empty = new Texture(new BaseTexture(img));
        for (var y=0;y<ROWS.length;y++) {
          for (var x=0;x<ROWS[y];x++) {
            let sprite = new Sprite(vm.tex_empty)
            sprite.index = i;
            sprite.interactive = true;
            sprite.on('mousedown', onDown);
            sprite.on('touchstart', onDown);
            sprite.x = sw*x+(9-ROWS[y])*0.5*sw + sw/2;
            sprite.y = sh*y + sh/2;
            sprite.width = sw;
            sprite.height = sh;
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
      for (const [index, element] of this.state.entries()) {
        let sprite = this.sprites[index];
        if (element[1] == null) {
          sprite.texture = this.tex_empty;
          sprite.cursor = 'pointer';
        } else if (element[1] == 0) {
          this.sprites[index].texture = this.tex_zero;
          sprite.cursor = 'grab';
        } else {
          this.sprites[index].texture = this.tex_one;
          sprite.cursor = 'grab';
        }
      }
      this.renderer.render(this.container)
    },
    surrender() {
      alert('WIRKLICH??!');
    },
  },
  created() {

  },
  mounted() {
    this.getMessage();
    this.getName();
    this.initGame();
    this.getGame();
    this.$root.$on('loadgame', (gid) => {
      console.log('Load', gid);
      this.gameid = gid;
      this.getGame();
    });
  },
};

</script>
