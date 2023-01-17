<template>
  <div id="app">
    <main-header></main-header>
    <main-input-field></main-input-field>
    <main-output-field></main-output-field>
    <main-footer></main-footer>
  </div>
</template>

<script>
import MainHeader from './components/MainHeader.vue'
import MainInputField from './components/MainInputField.vue'
import MainOutputField from './components/MainOutputField.vue'
import MainFooter from './components/MainFooter.vue'

export default {
  components: {
    'main-header': MainHeader,
    'main-input-field': MainInputField,
    'main-output-field': MainOutputField,
    'main-footer': MainFooter,
  }
}
</script>

<style>
@import './assets/styles/minireset.css';
@import './assets/styles/fonts.css';

* {
  font-family: NanumSquareNeo-bRg;
  background-color: #F5F5F5;
}
</style>