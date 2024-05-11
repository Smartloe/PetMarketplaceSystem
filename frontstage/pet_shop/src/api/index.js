import axios from 'axios'


// import {getBasicAuthHeader} from '@/utils/auth'

const instance = axios.create({
    baseURL: 'http://localhost:8010/api',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': getBasicAuthHeader()
    }
})

// 获取 Basic Auth 头部的工具函数
export function getBasicAuthHeader() {
    const username = localStorage.getItem('username')
    const password = localStorage.getItem('password')
    return 'Basic ' + btoa(`${username}:${password}`)
}

export const getCommodities = () => instance.get('/commodity/list/')
export const getCommodityDetail = (id) => instance.get(`/commodity/detail/${id}/`)
export const getAdvertisements = () => instance.get('/merchant/advertisements/')
export const addToCart = (data) => instance.post('/trade/shopping-carts/', data)
export const getCartItems = () => instance.get('/trade/shopping-carts/')
export const updateCartItem = (id, data) => instance.put(`/trade/shopping-carts/${id}/`, data)
export const removeCartItem = (id) => instance.delete(`/trade/shopping-carts/${id}/`)
export const placeOrder = (data) => instance.post('/trade/orders/', data)
export const getUserProfile = () => instance.get('/accounts/profiles/')
export const updateUserProfile = (data) => instance.put('/accounts/profiles/me/', data)
export const getUserFavorites = () => instance.get('/operation/favorites/')
export const addToFavorites = (data) => instance.post('/operation/favorites/', data)
export const removeFromFavorites = (id) => instance.delete(`/operation/favorites/${id}/`)
export const getUserMessages = () => instance.get('/operation/messages/')
export const createUserMessage = (data) => instance.post('/operation/messages/', data)
export const getUserOrders = () => instance.get('/trade/orders/')

