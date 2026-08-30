import {createRouter, createWebHistory} from 'vue-router'
import store from '@/store';
import {isAuthenticated} from '@/api';
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
    {path: '/favorites', component: Favorites, meta: {title: '我的收藏', requiresAuth: true}},
    {path: '/messages', component: Messages, meta: {title: '我的留言', requiresAuth: true}},
    {path: '/trade/orders', component: Orders, meta: {title: '我的订单', requiresAuth: true}},
    {path: '/trade/shopping-carts', component: ShoppingCart, meta: {title: '购物车', requiresAuth: true}},
    {path: '/accounts/user-center', component: UserCenter, meta: {title: '个人中心', requiresAuth: true}},
    {path: '/accounts/login', component: Login, meta: {title: '登录'}},
    {path: '/accounts/register', component: Register, meta: {title: '注册'}},
    {
        path: '/ai-pet-expert',
        name: 'AIPetExpert',
        component: AIPetExpert,
        // AI 问答接口要求登录，未登录直接引导去登录页
        meta: {title: 'AI 宠物顾问', requiresAuth: true}
    },
    // 未匹配到的路径回首页，避免白屏
    {path: '/:pathMatch(.*)*', redirect: '/'}
]
// 创建路由对象
const router = createRouter({
    // 设置历史记录模式
    history: createWebHistory(process.env.BASE_URL),
    routes
})

// 登录态以本地 token 为准，而不是 Vuex 里被持久化的布尔值：
// token 过期/清除后 isLoggedIn 仍可能停留在 true，导致 Header 显示
// 已登录但所有请求 401。
router.beforeEach((to) => {
    if (to.meta.requiresAuth && !isAuthenticated()) {
        if (store.state.isLoggedIn) {
            store.dispatch('logout');
        }
        return {path: '/accounts/login', query: {next: to.fullPath}};
    }
});

// 同步浏览器标签页标题
router.afterEach((to) => {
    document.title = to.meta.title ? `${to.meta.title} · 吉祥宠物商城` : '吉祥宠物商城';
});

export default router
