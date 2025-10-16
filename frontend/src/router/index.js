import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import RIRView from '@/views/RIRView.vue';
import SignalView from '@/views/SignalView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/analysis',
      name: 'analysis',
      component: RIRView,
    },
    {
      path: '/signal',
      name: 'signal',
      component: SignalView,
    },
    {
      path: '/convolve',
      redirect: '/analysis',
    },
  ],
});

export default router;