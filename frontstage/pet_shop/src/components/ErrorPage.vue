<template>

	<nav>
		<div class="menu">
			<p class="website_name">吉祥宠物商城</p>
		</div>
	</nav>
	<div class="wrapper">
		<div class="container">
			<div id="scene" class="scene" data-hover-only="false">
				<div class="circle" data-depth="1.2"></div>
				<div class="one" data-depth="0.9">
					<div class="content">
						<span class="piece"></span>
						<span class="piece"></span>
						<span class="piece"></span>
					</div>
				</div>
				<div class="two" data-depth="0.60">
					<div class="content">
						<span class="piece"></span>
						<span class="piece"></span>
						<span class="piece"></span>
					</div>
				</div>
				<div class="three" data-depth="0.40">
					<div class="content">
						<span class="piece"></span>
						<span class="piece"></span>
						<span class="piece"></span>
					</div>
				</div>
				<p class="p404" data-depth="0.50">404</p>
				<p class="p404" data-depth="0.10">404</p>
			</div>
			<div class="text">
				<article>
					<button>
						<router-link :to="`/`">返回首页</router-link>
					</button>
				</article>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "ErrorPage"
}
</script>

<style src="@/assets/style.css" scoped>
</style>
