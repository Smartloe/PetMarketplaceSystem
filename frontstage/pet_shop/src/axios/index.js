import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8010/api/';
axios.defaults.headers.post["Content-Type"] = 'application/json';
axios.defaults.headers.put["Content-Type"] = 'application/json'; // 确保 PUT 请求也设置了正确的 Content-Type
axios.defaults.timeout = 60000;
axios.defaults.withCredentials = true; // 允许跨域请求携带 cookie

// 获取 CSRF 令牌的函数
function getCSRFToken() {
    const csrfToken = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return csrfToken;
}

// 添加请求拦截器
axios.interceptors.request.use(function (config) {
    // 在发送请求之前添加 CSRF 令牌
    const csrfToken = getCSRFToken();
    if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
}, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
});

export default axios;