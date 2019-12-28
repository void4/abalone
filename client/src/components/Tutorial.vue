<template>
    <div>
      <h3>Tutorial</h3>
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
    };
  },
  components: {
  },
  methods: {
    getQuote() {
      const path = 'http://localhost:5000/quote';
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
