import {createStore} from 'vuex';
import createPersistedState from "vuex-persistedstate";

const store = createStore({
    state: {
        lookImgUrl: 'http://127.0.0.1:8000',
        userId: null, // 添加用户 ID 状态
        username: '',
        last_login: '',
        isLoggedIn: false, // 添加用户登录状态
    },
    mutations: {
        setUserId(state, userId) {
            state.userId = userId;
        },
        setUserName(state, username) {
            state.username = username;
        },
        setLastLogin(state, last_login) {
            state.last_login = last_login;
        },
        setIsLoggedIn(state, isLoggedIn) {
            state.isLoggedIn = isLoggedIn;
        },
    },
    actions: {
        logout({commit}) {
            // 清除用户信息和登录状态
            commit('setUserId', null);
            commit('setUserName', '');
            commit('setLastLogin', '');
            commit('setIsLoggedIn', false);
            // 可能还需要其他登出逻辑，比如清除 localStorage
        },
    },
    modules: {},
    // 所有数据缓存到本地
    plugins: [createPersistedState()],
});

export default store;