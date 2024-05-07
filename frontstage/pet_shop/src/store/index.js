import {createStore} from 'vuex'
import createPersistedState from "vuex-persistedstate";


const store = createStore({
    state: {
        lookImgUrl: 'http://127.0.0.1:8000',
        username: '',
        last_login: ''
    },
    mutations: {
        setUserName(state, username) {
            state.username = username
        },
        setLastLogin(state, last_login) {
            state.last_login = last_login
        },
    },
    actions: {},
    modules: {},
    // 所有数据缓存到本地
    plugins: [createPersistedState()],
})
export default store


