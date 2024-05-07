
import {createRouter, createWebHashHistory} from 'vue-router'
import Home from '../components/HomePage.vue'
import Commodity from '../components/CommodityItem.vue'
import Detail from '../components/CommodityDetail.vue'
import Shopper from '../components/ShopperProfile.vue'
import Login from '../components/LoginComponent.vue'
import Shopcart from '../components/ShoppingCart.vue'
import Error from '../components/ErrorPage.vue'

// 定义路由
const routes = [
    {path: '/', component: Home, meta: {title: '首页'}},
    {path: '/commodity', component: Commodity, meta: {title: '商品列表页'}},
    // :id是设置路由变量
    {path: '/commodity/detail/:id', component: Detail, meta: {title: '商品详细页'}},
    {path: '/shopper', component: Shopper, meta: {title: '个人中心页'}},
    {path: '/shopper/login', component: Login, meta: {title: '用户登录页'}},
    {path: '/shopper/shopcart', component: Shopcart, meta: {title: '我的购物车'}},
    // 路由匹配
    {path: '/:pathMatch(.*)*', component: Error, meta: {title: '页面丢失'}},
]

// 创建路由对象
const router = createRouter({
    // 设置历史记录模式
    history: createWebHashHistory(),
    // routes: routes的缩写
    routes,
})
export default router
