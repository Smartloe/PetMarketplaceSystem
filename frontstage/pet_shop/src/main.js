import {createApp} from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import base from './components/AppHeader.vue';
import footer from './components/AppFooter.vue';

// Element Plus 改为按需引入（见 vite.config.js 的 Components 插件），
// 不再全量注册。JS API 组件不经模板渲染，样式需要手动引入：
import 'element-plus/es/components/message/style/css';
import 'element-plus/es/components/message-box/style/css';

// 导入统一设计系统样式
import './assets/design-system.css';
import './assets/style.css';

// 动效指令 (v-reveal / v-tilt / v-parallax)
import { registerMotion } from './composables/motion';

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

// 注册全局动效指令
registerMotion(app);

// 注册全局组件
// 注意：不要在这里改全局 axios.defaults —— 业务请求全部走 src/api 的
// 独立实例，任何全局默认值（尤其 baseURL）都会污染它，历史上曾因此让
// token 刷新请求在生产环境打到 localhost:8010。
app.component('base-page', base);
app.component('footer-page', footer);

// 使用路由
app.use(router);

// 使用Vuex状态管理
app.use(store);

// 挂载Vue应用实例到DOM
app.mount('#app');
