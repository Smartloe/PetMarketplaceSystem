<template>
	<div class="ai-pet-expert-container">
		<iframe
			class="ai-pet-expert-iframe"
			src="https://www.coze.com/store/bot/7365143638118367248?bot_id=true"
			frameborder="0"
			allowfullscreen
		></iframe>
	</div>
</template>

<script>
export default {
	name: 'AIPetExpert'
};
</script>

<style scoped>
.ai-pet-expert-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 20px;
}

.ai-pet-expert-title {
	margin-bottom: 20px;
	font-size: 24px;
	font-weight: bold;
}

.ai-pet-expert-iframe {
	width: 100%;
	height: 80vh; /* 您可以根据需要调整高度 */
	border: none;
}
</style>