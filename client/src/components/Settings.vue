<template>
    <div>
      <h3>{{ $t('settings') }}</h3>
      <b-form-checkbox
        id="sound"
        v-model="$settings.sound"
        name="sound"
      >Sound</b-form-checkbox>
      <b-form-radio-group
        id="btn-radios-1"
        v-model="$i18n.locale"
        :options="options"
        buttons
        name="radios-btn-default"
      ></b-form-radio-group>
      <br>
      <img alt="◐" v-on:click="toggleDarkmode()" class="btn top-right" title="Switch between dark and light mode">
    </div>
</template>

<script>

export default {
  name: 'Settings',
  data() {
    return {
      options: [
        { text: 'English', value: 'en' },
        { text: 'Deutsch', value: 'de' },
      ],
    };
  },
  components: {
  },
  methods: {
    toggleDarkmode() {
      //var element = document.body;
      var elements = [document.body, document.getElementById('userbar'), document.getElementById('gamebar'), document.getElementById('sidebar')]
      for (var element of elements) {
        if (element !== null) {
          element.classList.toggle("dark-mode");
        }
      }
    },
  },
  mounted() {
  },
};

</script>
