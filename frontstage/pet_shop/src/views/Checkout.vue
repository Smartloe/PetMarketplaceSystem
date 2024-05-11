<template>
	<div class="checkout">
		<h2>填写收货地址</h2>
		<el-form :model="address" label-width="120px" @submit.prevent="placeOrder">
			<el-form-item label="收货人" required>
				<el-input v-model="address.signer_name"/>
			</el-form-item>
			<el-form-item label="手机号" required>
				<el-input v-model="address.signer_mobile"/>
			</el-form-item>
			<el-form-item label="所在地区" required>
				<el-cascader
					v-model="addressComponents"
					:options="regionOptions"
					@change="onAddressChange"
				/>
			</el-form-item>
			<el-form-item label="详细地址" required>
				<el-input v-model="address.address"/>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" @click="placeOrder">提交订单</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>

<script>
import {ref} from 'vue'
import axios from 'axios'

export default {
	name: 'Checkout',
	setup() {
		const address = ref({
			signer_name: '',
			signer_mobile: '',
			province: '',
			city: '',
			county: '',
			address: ''
		})
		const addressComponents = ref([])
		const regionOptions = ref([])

		// 获取地区选项
		axios.get('/api/operation/addresses/')
			.then(response => {
				const addresses = response.data.results
				const provinces = new Set()
				const cities = new Set()
				const counties = new Set()

				addresses.forEach(item => {
					provinces.add(item.province)
					cities.add(item.city)
					counties.add(item.county)
				})

				regionOptions.value = [
					{value: 'province', label: '省', options: Array.from(provinces)},
					{value: 'city', label: '市', options: Array.from(cities)},
					{value: 'county', label: '区/县', options: Array.from(counties)}
				]
			})
			.catch(error => {
				console.error('Error fetching region options:', error)
			})

		const onAddressChange = (value) => {
			address.value.province = value[0]
			address.value.city = value[1]
			address.value.county = value[2]
		}

		const placeOrder = () => {
			// 创建订单
			axios.post('/api/trade/orders/', {
				address: address.value.id,
				...其他订单信息
			})
				.then(response => {
					// 订单创建成功
					router.push(`/order/${response.data.id}`)
				})
				.catch(error => {
					console.error('Error creating order:', error)
				})
		}

		return {
			address,
			addressComponents,
			regionOptions,
			onAddressChange,
			placeOrder
		}
	}
}
</script>

<style scoped>
.checkout {
	padding: 20px;
}
</style>