<template>
	<div class="app-shell">
		<!-- Reading progress: a vermilion rule that fills as the page is read. -->
		<div
			class="read-progress"
			:style="{ '--read-progress': progress }"
			role="progressbar"
			aria-label="页面阅读进度"
			:aria-valuenow="Math.round(progress * 100)"
			aria-valuemin="0"
			aria-valuemax="100"
		></div>

		<Header/>
		<main class="app-main-shell">
			<router-view v-slot="{ Component, route }">
				<transition name="page" mode="out-in">
					<component :is="Component" :key="route.path"/>
				</transition>
			</router-view>
		</main>
		<Footer/>
	</div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { useScrollProgress } from '@/composables/motion'

export default {
	components: {
		Header,
		Footer
	},
	setup() {
		const { progress } = useScrollProgress()
		return { progress }
	}
}
</script>

<style scoped>
.read-progress {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	height: 2px;
	z-index: calc(var(--z-sticky) + 5);
	pointer-events: none;
	background: var(--vermilion);
	transform: scaleX(var(--read-progress, 0));
	transform-origin: left center;
	transition: transform 120ms linear;
}

/* Page transitions: a short paper-swap, not a slide show. */
.page-enter-active {
	transition: opacity 420ms cubic-bezier(0.16, 1, 0.3, 1),
		transform 420ms cubic-bezier(0.16, 1, 0.3, 1);
}

.page-leave-active {
	transition: opacity 200ms ease, transform 200ms ease;
}

.page-enter-from {
	opacity: 0;
	transform: translate3d(0, 14px, 0);
}

.page-leave-to {
	opacity: 0;
	transform: translate3d(0, -8px, 0);
}

@media (prefers-reduced-motion: reduce) {
	.page-enter-active,
	.page-leave-active {
		transition-duration: 1ms;
	}
}
</style>
