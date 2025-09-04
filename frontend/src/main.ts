import { createApp } from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import router from './router';
import './styles/main.scss';
import { restoreAuthFromStorage } from './store/auth';

const app = createApp(App);
app.use(vuetify);
app.use(router);
restoreAuthFromStorage();
app.mount('#app');
