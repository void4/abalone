<template>
    <div>
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
  },
  mounted() {
  },
};

</script>
