<template>
    <div>
      <h3>Tutorial</h3>
      <p>
      {{ $t('tut0') }}
      <br><br>
      {{ $t('tut1') }}
      <br><br>
      {{ $t('tut2') }}
      <br><br>
      {{ $t('tut3') }}
      <br><br>
      {{ $t('tut4') }}
      <br><br>
      </p>
      <b>{{ $t('quote') }}</b>

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
