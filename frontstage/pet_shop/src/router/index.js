import {createRouter, createWebHistory} from 'vue-router'
import CommodityList from '@/views/CommodityList.vue'
import CommodityDetail from '@/views/CommodityDetail.vue'
import Favorites from '@/views/Favorites.vue'
import Messages from '@/views/Messages.vue'
import Orders from '@/views/Orders.vue'
import ShoppingCart from '@/views/ShoppingCart.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Home from '@/views/Home.vue'
import UserCenter from '@/views/UserCenter.vue'
import AIPetExpert from '@/views/AIPetExpert.vue';
//定义路由
const routes = [
    {path: '/', component: Home, meta: {title: '首页'}},
    {path: '/commodity', component: CommodityList, meta: {title: '商品列表'}},
    // :id 是一个动态参数，可以匹配任意值,用来设置路由变量
    {path: '/commodity/detail/:id', component: CommodityDetail, name: 'CommodityDetail', meta: {title: '商品详情'}},
    {path: '/favorites', component: Favorites, meta: {title: '我的收藏'}},
    {path: '/messages', component: Messages, meta: {title: '我的留言'}},
    {path: '/trade/orders', component: Orders, meta: {title: '我的订单'}},
    {path: '/trade/shopping-carts', component: ShoppingCart, meta: {title: '购物车'}},
    {path: '/accounts/user-center', component: UserCenter, meta: {title: '个人中心'}},
    {path: '/accounts/login', component: Login, meta: {title: '登录'}},
    {path: '/accounts/register', component: Register, meta: {title: '注册'}},
    {
        path: '/ai-pet-expert',
        name: 'AIPetExpert',
        component: AIPetExpert
    }
]
// 创建路由对象
const router = createRouter({
    // 设置历史记录模式
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router