import {createRouter, createWebHistory} from 'vue-router';
import AuthPage from "@/views/AuthPage.vue";
import HomeView from "@/views/HomeView.vue";
import ResetPasswordPage from "@/views/ResetPasswordPage.vue";
import HomePage from "@/components/HomeView/HomePage.vue";
import Profile from "@/components/HomeView/Profile.vue";

// Create the router instance
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/auth', component: AuthPage},
        {path: '/reset-password', component: ResetPasswordPage},
        {
            path: '/', component: HomeView, children: [
                {path: '', component: HomePage},
                {path: '/profile', component: Profile},
            ]
        },
    ]
});

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token');
    if (to.path === '/reset-password') {
        next();
        return;
    }
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
