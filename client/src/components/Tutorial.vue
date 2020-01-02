<template>
    <div>
      <b-form-radio-group
        id="btn-radios-1"
        v-model="language"
        :options="options"
        buttons
        name="radios-btn-default"
      ></b-form-radio-group>
      <template v-if="language == 'en'">
        <h3>Tutorial</h3>
        <p>
        1,2 or 3 marbles can be moved.
        <br><br>
        The objective of the game is to push 6 marbles of the opponent off the board.
        <br><br>
        To move the opponents' marbles, you always need to push with one more - 3 own can push 2 or 1 marbles, 2 can push 1 marble of the opponent.
        <br><br>
        To move marbles in the direction of a line, select the last one and then the field on which they are moved.
        <br><br>
        To move marbles sideways, select all of them and then, the field in which direction they should be moved - relative to the last selected marble.
        <br><br>
        </p>
        <br>
        <b>Quote of the day:</b>
      </template>
      <template v-if="language == 'de'">
        <p>
        Es können 1,2 oder 3 Kugeln geschoben werden.
        <br><br>
        Ziel des Spiels ist es 6 Kugeln des Gegners aus dem Spielfeld zu schieben.
        <br><br>
        Um gegnerische Kugeln zu verschieben, benötigt man immer eine mehr, 3 eigene können 2 oder 1 Kugel des Gegners schieben, 2 eine.
        <br><br>
        Zum Verschieben von Kugeln in einer Reihe: erst die hinterste Kugel auswählen und dann die Kugel/das Feld auf das geschoben werden soll.
        <br><br>
        Beim seitlichen Verschieben: Alle Kugeln die verschoben werden sollen auswählen und dann das Feld in dessen Richtung von der letzten Kugel aus verschoben werden soll.
        <br><br>
        </p>
        <br>
        <b>Zitat des Tages:</b>
      </template>

      {{ quote }}
    </div>
</template>

<style scoped>
p {
  text-align: left;
  margin: 5%;
}
</style>

<script>
import axios from 'axios';
import cookie from 'cookie-machine';


export default {
  name: 'Tutorial',
  data() {
    return {
      quote: '-',
      language: 'en',
      options: [
        { text: 'English', value: 'en' },
        { text: 'Deutsch', value: 'de' },
      ],
    };
  },
  components: {
  },
  methods: {
    getQuote() {
      const path = `${window.location.protocol}//${window.location.hostname}:5000/quote`;
      axios.get(path)
        .then((res) => {
          this.quote = res.data.quote;
        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
  },
  mounted() {
    this.getQuote();
  },
};

</script>
