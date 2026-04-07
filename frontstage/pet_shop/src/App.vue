<template>
	<div class="app-shell">
		<Header/>
		<main class="app-main-shell">
			<router-view/>
		</main>
		<Footer/>
	</div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
	components: {
		Header,
		Footer
	}
}
</script>
