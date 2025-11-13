# 🐾 吉祥宠物商城系统 - 开发文档

## 📚 详细开发指南

### 🔧 数据库设计

#### 核心数据表

##### 用户相关表
```sql
-- 用户基础信息表
CREATE TABLE accounts_userprofile (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254),
    phone VARCHAR(20),
    avatar VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 用户地址表
CREATE TABLE customer_operation_useraddress (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    province VARCHAR(100),
    city VARCHAR(100),
    district VARCHAR(100),
    address TEXT,
    signer_name VARCHAR(100),
    signer_mobile VARCHAR(20),
    is_default BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES accounts_userprofile(id)
);
```

##### 商品相关表
```sql
-- 商品信息表
CREATE TABLE commodity_commodityinfos (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    cost_price DECIMAL(10,2),
    market_price DECIMAL(10,2),
    shop_price DECIMAL(10,2),
    goods_sn VARCHAR(50) UNIQUE,
    click_num INT DEFAULT 0,
    sold_num INT DEFAULT 0,
    fav_num INT DEFAULT 0,
    goods_num INT DEFAULT 0,
    is_new BOOLEAN DEFAULT FALSE,
    is_hot BOOLEAN DEFAULT FALSE,
    goods_front_image VARCHAR(200),
    goods_detail_image VARCHAR(200),
    add_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 商品分类表
CREATE TABLE commodity_goodscategory (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    code VARCHAR(30),
    desc TEXT,
    category_type INT,
    parent_category_id BIGINT,
    is_tab BOOLEAN DEFAULT FALSE,
    add_time DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

##### 交易相关表
```sql
-- 购物车表
CREATE TABLE trade_shoppingcart (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    goods_id BIGINT NOT NULL,
    nums INT NOT NULL,
    add_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES accounts_userprofile(id),
    FOREIGN KEY (goods_id) REFERENCES commodity_commodityinfos(id)
);

-- 订单信息表
CREATE TABLE trade_orderinfo (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    order_sn VARCHAR(30) UNIQUE,
    trade_no VARCHAR(100),
    pay_status VARCHAR(30) DEFAULT 'TRADE_BUYER_PAID',
    post_script VARCHAR(200),
    order_mount DECIMAL(10,2),
    pay_time DATETIME,
    address VARCHAR(100),
    signer_name VARCHAR(20),
    singer_mobile VARCHAR(11),
    add_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES accounts_userprofile(id)
);
```

### 🔌 API接口文档

#### 认证接口

##### 用户注册
```http
POST /api/accounts/register/
Content-Type: application/json

{
    "username": "testuser",
    "password": "password123",
    "email": "test@example.com",
    "phone": "13800138000"
}
```

##### 用户登录
```http
POST /api/accounts/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "password123"
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }
}
```

#### 商品接口

##### 获取商品列表
```http
GET /api/commodity/goods/
Authorization: Bearer <access_token>

Query Parameters:
- page: 页码 (默认: 1)
- page_size: 每页数量 (默认: 12)
- search: 搜索关键词
- category: 分类ID
- ordering: 排序方式 (price, -price, add_time, -add_time)

Response:
{
    "count": 100,
    "next": "http://localhost:8010/api/commodity/goods/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "宠物玩具",
            "shop_price": "29.90",
            "goods_front_image": "/media/product_photos/goods_01.png",
            "is_new": true,
            "is_hot": false
        }
    ]
}
```

##### 获取商品详情
```http
GET /api/commodity/goods/{id}/
Authorization: Bearer <access_token>

Response:
{
    "id": 1,
    "name": "宠物玩具",
    "description": "高质量宠物玩具，安全无毒",
    "shop_price": "29.90",
    "market_price": "39.90",
    "goods_front_image": "/media/product_photos/goods_01.png",
    "goods_detail_image": "/media/product_photos_details/goods_details_01.png",
    "goods_num": 100,
    "sold_num": 50,
    "fav_num": 20
}
```

#### 购物车接口

##### 添加到购物车
```http
POST /api/trade/shopping-carts/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "goods": 1,
    "nums": 2
}
```

##### 获取购物车列表
```http
GET /api/trade/shopping-carts/
Authorization: Bearer <access_token>

Response:
{
    "count": 2,
    "results": [
        {
            "id": 1,
            "goods": {
                "id": 1,
                "name": "宠物玩具",
                "shop_price": "29.90",
                "goods_front_image": "/media/product_photos/goods_01.png"
            },
            "nums": 2,
            "add_time": "2024-01-01T10:00:00Z"
        }
    ]
}
```

#### AI对话接口

##### 发送消息
```http
POST /api/ai-chat/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "message": "我的猫咪不吃饭怎么办？",
    "conversation_id": "uuid-string" // 可选，用于维持对话上下文
}

Response (流式):
data: {"type": "message", "content": "您好！猫咪不吃饭可能有以下几个原因：\n\n"}
data: {"type": "message", "content": "1. **环境变化**：搬家、新宠物等环境变化可能导致猫咪食欲不振\n"}
data: {"type": "message", "content": "2. **健康问题**：口腔疾病、消化问题等\n"}
data: {"type": "end"}
```

### 🎨 前端组件开发

#### 通用组件规范

##### 按钮组件使用
```vue
<template>
  <!-- 主要按钮 -->
  <button class="pet-btn pet-btn-primary">
    <el-icon><Plus /></el-icon>
    添加到购物车
  </button>
  
  <!-- 次要按钮 -->
  <button class="pet-btn pet-btn-secondary">
    查看详情
  </button>
  
  <!-- 成功按钮 -->
  <button class="pet-btn pet-btn-success">
    确认订单
  </button>
  
  <!-- 小尺寸按钮 -->
  <button class="pet-btn pet-btn-primary pet-btn-sm">
    编辑
  </button>
</template>
```

##### 卡片组件使用
```vue
<template>
  <div class="pet-card">
    <div class="pet-card-header">
      <h3 class="pet-card-title">商品名称</h3>
      <p class="pet-card-subtitle">商品描述</p>
    </div>
    
    <div class="pet-card-body">
      <!-- 卡片内容 -->
    </div>
  </div>
</template>
```

##### 表单组件使用
```vue
<template>
  <div class="pet-form-group">
    <label class="pet-form-label">商品名称</label>
    <input 
      type="text" 
      class="pet-form-input" 
      placeholder="请输入商品名称"
      v-model="productName"
    />
  </div>
</template>
```

#### 状态管理 (Vuex)

##### Store结构
```javascript
// store/index.js
export default createStore({
  state: {
    user: null,
    isLoggedIn: false,
    cart: [],
    products: []
  },
  
  mutations: {
    SET_USER(state, user) {
      state.user = user;
      state.isLoggedIn = !!user;
    },
    
    ADD_TO_CART(state, product) {
      const existingItem = state.cart.find(item => item.id === product.id);
      if (existingItem) {
        existingItem.quantity += product.quantity;
      } else {
        state.cart.push(product);
      }
    },
    
    REMOVE_FROM_CART(state, productId) {
      state.cart = state.cart.filter(item => item.id !== productId);
    }
  },
  
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await api.post('/accounts/login/', credentials);
        const { access, refresh, user } = response.data;
        
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        
        commit('SET_USER', user);
        return response.data;
      } catch (error) {
        throw error;
      }
    },
    
    async addToCart({ commit }, product) {
      try {
        await api.post('/trade/shopping-carts/', {
          goods: product.id,
          nums: product.quantity
        });
        commit('ADD_TO_CART', product);
      } catch (error) {
        throw error;
      }
    }
  }
});
```

### 🔒 安全配置

#### Django安全设置
```python
# settings.py

# CORS配置
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8011",
    "http://127.0.0.1:8011",
]

CORS_ALLOW_CREDENTIALS = True

# JWT配置
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# 安全中间件
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 安全设置
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

#### 前端安全配置
```javascript
// axios配置
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8010/api',
  timeout: 10000,
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// 响应拦截器
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // Token过期，尝试刷新
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post('/accounts/token/refresh/', {
          refresh: refreshToken
        });
        
        localStorage.setItem('access_token', response.data.access);
        return api.request(error.config);
      } catch (refreshError) {
        // 刷新失败，跳转到登录页
        localStorage.clear();
        window.location.href = '/accounts/login';
      }
    }
    return Promise.reject(error);
  }
);
```

### 🧪 测试指南

#### 后端测试
```python
# tests/test_models.py
from django.test import TestCase
from accounts.models import UserProfile

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))

# tests/test_views.py
from rest_framework.test import APITestCase
from rest_framework import status

class ProductAPITestCase(APITestCase):
    def test_get_products(self):
        response = self.client.get('/api/commodity/goods/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

#### 前端测试
```javascript
// tests/unit/components/ProductCard.spec.js
import { mount } from '@vue/test-utils';
import ProductCard from '@/components/ProductCard.vue';

describe('ProductCard.vue', () => {
  it('renders product information correctly', () => {
    const product = {
      id: 1,
      name: 'Test Product',
      price: '29.90',
      image: '/test-image.jpg'
    };
    
    const wrapper = mount(ProductCard, {
      props: { product }
    });
    
    expect(wrapper.text()).toContain('Test Product');
    expect(wrapper.text()).toContain('29.90');
  });
});
```

### 📊 性能优化

#### 后端优化
```python
# 数据库查询优化
from django.db import models

class ProductViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return CommodityInfos.objects.select_related(
            'category'
        ).prefetch_related(
            'images'
        ).filter(is_active=True)

# 缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# 使用缓存
from django.core.cache import cache

def get_hot_products():
    cache_key = 'hot_products'
    products = cache.get(cache_key)
    
    if products is None:
        products = CommodityInfos.objects.filter(
            is_hot=True
        ).order_by('-sold_num')[:10]
        cache.set(cache_key, products, 300)  # 缓存5分钟
    
    return products
```

#### 前端优化
```javascript
// 路由懒加载
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('@/views/Products.vue')
  }
];

// 图片懒加载
<template>
  <img 
    v-lazy="product.image" 
    :alt="product.name"
    class="product-image"
  />
</template>

// 虚拟滚动（大列表优化）
<template>
  <virtual-list
    :data-sources="products"
    :data-key="'id'"
    :keeps="30"
    :estimate-size="200"
  >
    <template #ite{ record }">
      <ProductCard :product="record" />
    </template>
  </virtual-list>
</template>
```

### 🚀 #### Docker配置
```dockerfile
# Dockerfile.backend
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r rents.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "pet_shop.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```dockerfile
# Dockerfile.frontend
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN nuild

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: pet_shop
      MYSQL_ROOT_PASSWORD: password
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  backend:
    build:
      context: ./backstage/pet_shop
      dockerfile: Dockerfile
    depends_on:
      - db
    environment:
      - DB_HOST=db
      - DB_NAME=pet_shop
      - DB_USER=root
      - DB_PASSWORD=password
    ports:
      - "8000:8000"

  frontend:
    build:
      context: ./frontstage/pet_shop
      dockerfile: Dockerfile
    ports:
      - "80:80"

volumes:
  mysql_data:
```

### 📈 监控和日志

#### 日志配置
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

这份开发文档提供了项目的详细技术实现指南，包括数据库设计、API接口、前端组件、安全配置、测试方法、性能优化和部署实践。开发者可以根据这份文档快速上手项目开发和维护。