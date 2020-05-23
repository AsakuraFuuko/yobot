import Vue from 'vue';
import Vuerouter from 'vuerouter';
import ElementUI from 'element-ui';
import App from './App.vue';
import User from './User.vue';
import Clan from './Clan.vue';

const router = new Vuerouter({
  mode: 'history',
  routes: [
    {
      path: '/user',
      component: User,
    },
    {
      path: '/clan',
      component: Clan,
    },
  ]
})

Vue.use(ElementUI);

new Vue({
  el: '#app',
  router: router,
  render: h => h(App),
});