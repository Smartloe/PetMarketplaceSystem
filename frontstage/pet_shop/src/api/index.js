import axios from 'axios'

// 创建 axios 实例
const instance = axios.create({
    baseURL: 'http://localhost:8010/api',
    headers: {
        'Content-Type': 'application/json',
        // 注意：这里假设你在其他地方定义了 getBasicAuthHeader 函数
        // 如果你的API使用其他认证方式，比如Bearer token，你需要相应地修改这里
        'Authorization': getBasicAuthHeader()
    }
})

// 获取 Basic Auth 头部的工具函数
export function getBasicAuthHeader() {
    const username = localStorage.getItem('username')
    const password = localStorage.getItem('password')
    // 注意：确保username和password存在，否则btoa将抛出异常
    return username && password ? 'Basic ' + btoa(`${username}:${password}`) : null;
}

// 获取商品列表
export const getCommodities = () => instance.get('/commodity/list/')

// 搜索商品
export const searchCommodities = (query) => instance.get(`/commodity/search/`, {params: {query}})

// 获取商品详情
export const getCommodityDetail = (id) => instance.get(`/commodity/detail/${id}/`)

// 获取指定商品的评论列表
export const getCommodityComments = (commodityId) => instance.get(`/commodity/comments/${commodityId}/`)


// 获取广告列表
export const getAdvertisements = () => instance.get('/merchant/advertisements/')

// 添加商品到购物车
export const addToCart = (data) => instance.post('/trade/shopping-carts/', data)

// 获取购物车中的商品
export const getCartItems = () => instance.get('/trade/shopping-carts/')

// 更新购物车中的商品
export const updateCartItem = (id, data) => instance.put(`/trade/shopping-carts/${id}/`, data)

// 从购物车中移除商品
export const removeCartItem = (id) => instance.delete(`/trade/shopping-carts/${id}/`)

// 下单
export const placeOrder = (data) => instance.post('/trade/orders/', data)

// 获取用户个人信息
export const getUserProfile = () => instance.get('/accounts/profiles/')

// 更新用户个人信息
export const updateUserProfile = (id, data) => instance.put(`/accounts/profiles/${id}/`, data)

// 获取用户收藏列表
export const getUserFavorites = () => instance.get('/operation/favorites/')

// 添加商品到用户收藏
export const addToFavorites = (data) => instance.post('/operation/favorites/', data)

// 从用户收藏中移除商品
export const removeFromFavorites = (id) => instance.delete(`/operation/favorites/${id}/`)

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

// 获取订单列表
export const getUserOrders = () => axios.get('/trade/orders/');

// 获取订单详情
export const getOrderDetail = (id) => axios.get(`/trade/orders/${id}/`);

// 获取订单商品列表
export const getOrderGoods = (orderId) => axios.get(`/trade/order-goods/`, {params: {order: orderId}});

// 获取用户评论列表
export const getUserComments = () => instance.get('/operation/usercomments/')

// 创建新的用户评论
export const createUserComment = (data) => instance.post('/operation/usercomments/', data)

// 获取单个用户评论详情
export const getUserCommentDetail = (id) => instance.get(`/operation/usercomments/${id}/`)

// 更新用户评论
export const updateUserComment = (id, data) => instance.put(`/operation/usercomments/${id}/`, data)

// 部分更新用户评论
export const partialUpdateUserComment = (id, data) => instance.patch(`/operation/usercomments/${id}/`, data)

// 删除用户评论
export const deleteUserComment = (id) => instance.delete(`/operation/usercomments/${id}/`)

// 用户注册
export const registerUser = (data) => instance.post('/accounts/register/', data)

// 获取验证码
export const getCaptcha = (username) => instance.get('/accounts/captcha/', {params: {username}});

// 用户登录
export const loginUser = (data) => instance.post('/accounts/login/', data)
