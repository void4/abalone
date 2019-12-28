<template>
    <div>
        <img alt="Vue logo" src="../assets/face.png">
        <p>{{ msg }}</p>
        <vue-dropzone ref="myVueDropzone" id="dropzone" :options="dropzoneOptions"></vue-dropzone>
    </div>
</template>

<script>
import vue2Dropzone from 'vue2-dropzone';
import 'vue2-dropzone/dist/vue2Dropzone.min.css';
import axios from 'axios';


export default {
  name: 'Ping',
  data() {
    return {
      msg: '-',
      name: '?',
      game: '-',
      dropzoneOptions: {
        url: '',
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        headers: { 'My-Awesome-Header': 'header value' },
      },
    };
  },
  components: {
    vueDropzone: vue2Dropzone,
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
  mounted() {
    this.getMessage();
  },
};
</script>
