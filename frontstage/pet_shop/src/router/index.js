import {createRouter, createWebHistory} from 'vue-router'
import CommodityList from '@/views/CommodityList.vue'
import CommodityDetail from '@/views/CommodityDetail.vue'
import Favorites from '@/views/Favorites.vue'
import Messages from '@/views/Messages.vue'
import Orders from '@/views/Orders.vue'
import ShoppingCart from '@/views/ShoppingCart.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'

const routes = [
    {path: '/commodity/list', component: CommodityList},
    {path: '/commodity/detail/:id', component: CommodityDetail},
    {path: '/operation/favorites', component: Favorites},
    {path: '/operation/messages', component: Messages},
    {path: '/trade/orders', component: Orders},
    {path: '/trade/shopping-carts', component: ShoppingCart},
    {path: '/accounts/login', component: Login},
    {path: '/accounts/register', component: Register},
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router