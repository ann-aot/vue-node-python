import { createApp } from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import router from './router';
import './styles/main.scss';
import store from './store';
import axios from 'axios';

// Force HTTPS for Gitpod environment to prevent mixed content errors
if (window.location.hostname.includes('gitpod.io')) {
  axios.interceptors.request.use((config) => {
    if (config.url && config.url.startsWith('http://') && config.url.includes('gitpod.io')) {
      console.log('Forcing HTTPS for Gitpod request:', config.url);
      config.url = config.url.replace('http://', 'https://');
    }
    return config;
  });
}

const app = createApp(App);
app.use(vuetify);
app.use(router);
app.use(store);
app.mount('#app');
