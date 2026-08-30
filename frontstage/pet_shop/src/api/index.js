import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

// 创建 axios 实例
const instance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: true
});

// 刷新 token 必须用完全独立的实例：既不经过 instance 的拦截器，也
// 不继承任何全局 axios.defaults——此前遗留模块把全局 baseURL 改写成
// http://localhost:8010/api/，导致生产环境的刷新请求必然 404，用户
// access token 一过期就被强制登出。
const bareAxios = axios.create();

// ---- token 存取 ----
// 只保存 JWT。此前这里保存的是明文密码并对每个请求做 Basic Auth，
// 任何一次 XSS 都能拿到可无限复用的真实凭据；JWT 至少是有期限、
// 可作废的。

export function getAccessToken() {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function setAuthTokens({ access, refresh }) {
    if (access) {
        localStorage.setItem(ACCESS_TOKEN_KEY, access);
    }
    if (refresh) {
        localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
    }
}

export function clearAuthTokens() {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    // 清掉旧版本遗留的明文凭据
    localStorage.removeItem('username');
    localStorage.removeItem('password');
}

export function isAuthenticated() {
    return Boolean(getAccessToken());
}

instance.interceptors.request.use((config) => {
    const token = getAccessToken();
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    } else {
        delete config.headers.Authorization;
    }
    return config;
});

// ---- access token 过期时自动刷新并重放原请求 ----
// 并发的 401 共享同一次刷新，避免同时打多个 refresh 请求。
let refreshInFlight = null;

function refreshAccessToken() {
    const refresh = getRefreshToken();
    if (!refresh) {
        return Promise.reject(new Error('no refresh token'));
    }
    if (!refreshInFlight) {
        // 用裸实例，避免走到本实例的拦截器造成递归
        refreshInFlight = bareAxios
            .post(`${API_BASE_URL}/accounts/token/refresh/`, { refresh })
            .then((response) => {
                const access = response.data.access;
                setAuthTokens({ access, refresh: response.data.refresh });
                return access;
            })
            .finally(() => {
                refreshInFlight = null;
            });
    }
    return refreshInFlight;
}

instance.interceptors.response.use(
    (response) => response,
    (error) => {
        const { response, config } = error;
        const isAuthFailure = response && response.status === 401;
        const isRefreshCall = config && config.url && config.url.includes('/token/refresh/');

        if (!isAuthFailure || isRefreshCall || !config || config._retried) {
            return Promise.reject(error);
        }

        return refreshAccessToken()
            .then((access) => {
                config._retried = true;
                config.headers = config.headers || {};
                config.headers.Authorization = `Bearer ${access}`;
                return instance.request(config);
            })
            .catch(() => {
                // refresh 也失效了：清空并让调用方决定如何跳转
                clearAuthTokens();
                return Promise.reject(error);
            });
    }
);

// 获取商品列表
export const getCommodities = () => instance.get('/commodity/list/');

// 搜索商品
export const searchCommodities = (query) => instance.get(`/commodity/search/`, { params: { query } });

// 获取商品详情
export const getCommodityDetail = (id) => instance.get(`/commodity/detail/${id}/`);

// 获取指定商品的评论列表
export const getCommodityComments = (commodityId) => instance.get(`/commodity/comments/${commodityId}/`);

// 获取广告列表
export const getAdvertisements = () => instance.get('/merchant/advertisements/');

// 添加商品到购物车
export const addToCart = (data) => instance.post('/trade/shopping-carts/', data);

// 获取购物车中的商品
export const getCartItems = () => instance.get('/trade/shopping-carts/');

// 更新购物车中的商品
export const updateCartItem = (id, data) => instance.put(`/trade/shopping-carts/${id}/`, data);

// 从购物车中移除商品
export const removeCartItem = (id) => instance.delete(`/trade/shopping-carts/${id}/`);

// 获取订单列表
export const getUserOrders = () => instance.get('/trade/orders/');

// 获取订单详情
export const getOrderDetail = (id) => instance.get(`/trade/orders/${id}/`);

// 删除订单（后端仅允许取消待支付订单）
export const deleteOrder = (id) => instance.delete(`/trade/orders/${id}/`);

// 模拟支付。订单状态只能走后端专用端点流转，直接 PUT /trade/orders/
// 改状态已被关闭（会 405），因为通用写接口曾被用来篡改金额和状态。
export const payOrderRequest = (id, data) => instance.post(`/trade/orders/${id}/pay/`, data);

// 撤销退款申请（仅“待审核”状态可撤，订单回到发货中）
export const cancelOrderRefund = (id) => instance.post(`/trade/orders/${id}/refund/cancel/`);

// 获取订单商品列表
export const getOrderGoods = (orderId) => instance.get(`/trade/order-goods/`, { params: { order: orderId } });

// 获取用户个人信息
export const getUserProfile = () => instance.get('/accounts/profiles/');

// 更新用户个人信息
export const updateUserProfile = (id, data) => instance.put(`/accounts/profiles/${id}/`, data);

// 获取用户收藏列表
export const getUserFavorites = () => instance.get('/operation/favorites/');

// 添加商品到用户收藏
export const addToFavorites = (data) => instance.post('/operation/favorites/', data);

// 从用户收藏中移除商品
export const removeFromFavorites = (id) => instance.delete(`/operation/favorites/${id}/`);

// 获取用户留言列表
export const getUserMessages = () => instance.get('/operation/messages/');

// 创建用户留言
export const createUserMessage = (data) => instance.post('/operation/messages/', data);

// 更新用户留言
export const updateUserMessage = (id, data) => instance.put(`/operation/messages/${id}/`, data);

// 删除用户留言
export const deleteUserMessage = (id) => instance.delete(`/operation/messages/${id}/`);

// 获取单个用户留言详情
export const getUserMessageDetail = (id) => instance.get(`/operation/messages/${id}/`);

// 获取用户评论列表
export const getUserComments = () => instance.get('/operation/usercomments/');

// 创建新的用户评论
export const createUserComment = (data) => instance.post('/operation/usercomments/', data);

// 获取单个用户评论详情
export const getUserCommentDetail = (id) => instance.get(`/operation/usercomments/${id}/`);

// 更新用户评论
export const updateUserComment = (id, data) => instance.put(`/operation/usercomments/${id}/`, data);

// 部分更新用户评论
export const partialUpdateUserComment = (id, data) => instance.patch(`/operation/usercomments/${id}/`, data);

// 删除用户评论
export const deleteUserComment = (id) => instance.delete(`/operation/usercomments/${id}/`);

// 用户注册
export const registerUser = (data) => instance.post('/accounts/register/', data);

// 获取验证码
export const getCaptcha = (username) => instance.get('/accounts/captcha/', { params: { username } });

// 用户登录
export const loginUser = (data) => instance.post('/accounts/login/', data);

// 用户登出。后端路由是 /loginout/（不是 /logout/），此前这里写错导致
// 登出请求一直静默 404。JWT 是无状态的，真正的登出动作是本地清 token。
export const logoutUser = () => instance.post('/accounts/loginout/').finally(clearAuthTokens);

// 获取用户地址列表
export const getUserAddresses = (page) => instance.get('/operation/addresses/', { params: { page } });

// 创建用户地址
export const createUserAddress = (data) => instance.post('/operation/addresses/', data);

// 获取单个用户地址详情
export const getUserAddress = (id) => instance.get(`/operation/addresses/${id}/`);

// 更新用户地址
export const updateUserAddress = (id, data) => instance.put(`/operation/addresses/${id}/`, data);

// 部分更新用户地址
export const partialUpdateUserAddress = (id, data) => instance.patch(`/operation/addresses/${id}/`, data);

// 删除用户地址
export const deleteUserAddress = (id) => instance.delete(`/operation/addresses/${id}/`);
export const getRegions = () => instance.get('/operation/regions/');
export const uploadAvatar = (formData) => instance.post('/accounts/profiles/upload-avatar/', formData, {
    headers: {'Content-Type': 'multipart/form-data'}
});

// AI 宠物顾问
export const consultPetAdvisor = (payload) => instance.post('/ai/consult/', payload);

// 结算下单（伪支付）
export const checkoutOrder = (payload) => instance.post('/trade/checkout/', payload);
export const requestOrderRefund = (orderId, payload) => instance.post(`/trade/orders/${orderId}/refund/`, payload);
export const confirmOrder = (orderId) => instance.post(`/trade/orders/${orderId}/confirm/`);
export const commentOrderGoods = (orderId, orderGoodsId, payload) => instance.post(`/trade/orders/${orderId}/goods/${orderGoodsId}/comment/`, payload);
