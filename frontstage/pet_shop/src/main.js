import {createApp} from 'vue';
import VueAxios from 'vue-axios';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from './axios';
import base from './components/Header.vue';
import footer from './components/Footer.vue';

// 导入Element Plus库及其样式
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

// 导入统一设计系统样式
import './assets/design-system.css';

// 防抖函数
const debounce = (fn, delay) => {
    let timer = null;
    return function () {
        let context = this;
        let args = arguments;
        clearTimeout(timer);
        timer = setTimeout(function () {
            fn.apply(context, args);
        }, delay);
    }
}

// 重写 ResizeObserver
const _ResizeObserver = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends _ResizeObserver {
    constructor(callback) {
        callback = debounce(callback, 16);
        super(callback);
    }
}

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