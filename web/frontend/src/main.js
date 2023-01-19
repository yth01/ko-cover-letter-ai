import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueClipboard from 'vue-clipboard2'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faGithub } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import axios from 'axios'

Vue.prototype.$EventBus = new Vue();
Vue.prototype.$axios = axios;

library.add(faGithub)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

VueClipboard.config.autoSetContainer = true
Vue.use(VueClipboard)

new Vue({
  vuetify,
  render: h => h(App),
}).$mount('#app')

