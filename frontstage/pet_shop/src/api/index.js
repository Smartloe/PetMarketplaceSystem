import axios from 'axios'

const instance = axios.create({
    baseURL: 'http://localhost:8000/api/',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
})

export const loginUser = (username, password, code) => {
    return instance.post('/accounts/login/', {username, password, code})
}

export const registerUser = (username, email, password, password2) => {
    return instance.post('/accounts/register/', {username, email, password, password2})
}

// 添加其他 API 调用方法