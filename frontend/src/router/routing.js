import {createRouter, createWebHistory} from 'vue-router';
import AuthPage from "@/views/AuthPage.vue";
import HomePage from "@/views/HomePage.vue";

// Create the router instance
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/auth', component: AuthPage},
        {path: '/', component: HomePage},
        {path: '/home', redirect: HomePage},
    ]
});

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token');
    if (token) {
        if (to.path === '/auth') {
            next('/');
        } else {
            next();
        }
    } else {
        if (to.path !== '/auth') {
            next('/auth');
        } else {
            next();
        }
    }
});

export default router;
