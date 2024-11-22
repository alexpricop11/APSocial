import {createRouter, createWebHashHistory} from 'vue-router';
import AuthPage from "@/components/auth/AuthPage.vue";
import Home from "@/components/home/Home.vue";

const routes = [
    {path: '/home', component: Home, name: 'Home'},
    {path: '/auth-page', component: AuthPage},
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;
