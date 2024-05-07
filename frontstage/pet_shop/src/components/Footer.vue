<template>
	<div class="footer">
		<el-row class="ng-promise-box" justify="center">
			<el-col :span="16">
				<div class="ng-promise">
					<el-link class="icon1" icon="el-icon-goods" :underline="false">7天无理由退换货</el-link>
					<el-link class="icon2" icon="el-icon-truck" :underline="false">满99元全场免邮</el-link>
					<el-link class="icon3" icon="el-icon-s-check" :underline="false">100%品质保证</el-link>
				</div>
			</el-col>
		</el-row>
		<el-row class="mod_help" justify="center">
			<el-col :span="16">
				<div style="text-align: center; padding: 20px 0;">
					<el-link href="javascript:;" :underline="false">关于我们</el-link>
					<span>|</span>
					<el-link href="javascript:;" :underline="false">帮助中心</el-link>
					<span>|</span>
					<el-link href="javascript:;" :underline="false">售后服务</el-link>
					<span>|</span>
					<el-link href="javascript:;" :underline="false">宠物资讯</el-link>
					<span>|</span>
					<el-link href="javascript:;" :underline="false">关于货源</el-link>
				</div>
			</el-col>
		</el-row>
	</div>
</template>

<script>
export default {
	name: "AppFooter"
}
</script>

<style scoped>
.ng-promise-box {
	padding: 20px 0;
	background-color: #f5f5f5;
}

.ng-promise {
	display: flex;
	justify-content: space-between;
	text-align: center;
}

.mod_help {
	background-color: #333;
	color: #fff;
}

.mod_help a {
	color: #fff;
}

.mod_help span {
	margin: 0 10px;
}
</style>