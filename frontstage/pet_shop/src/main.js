import {createApp} from 'vue';
import VueAxios from 'vue-axios';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from './axios';
import base from './components/BaseComponent.vue';
import footer from './components/Footer.vue';

// 导入Element Plus库及其样式
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

// 创建Vue应用实例
const app = createApp(App);

// 全局使用Element Plus
app.use(ElementPlus);

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
// 注册全局组件
app.component('base-page', base);
app.component('footer-page', footer);

// 使用路由
app.use(router);

// 使用Vuex状态管理
app.use(store);

// 使用vue-axios
app.use(VueAxios, axios);

// 挂载Vue应用实例到DOM
app.mount('#app');