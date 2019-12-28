<template>
    <div>
        Statistics
        {{ msg }}
        <img alt="Vue logo" src="../assets/graph.png">
    </div>
</template>

<script>
import axios from 'axios';


export default {
  name: 'Stats',
  data() {
    return {
      msg: '-',
    };
  },
  components: {
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
  },
  created() {
    this.getMessage();
  },
};
</script>
