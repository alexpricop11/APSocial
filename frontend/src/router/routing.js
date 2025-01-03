import {createRouter, createWebHistory} from 'vue-router';
import AuthPage from "@/views/AuthPage.vue";
import HomeView from "@/views/HomeView.vue";
import HomePage from "@/components/Home/HomePage.vue";
import Profile from "@/components/Profile/Profile.vue";
import Search from "@/components/Search.vue";
import Chat from "@/components/Chat.vue";
import Notifications from "@/components/Notifications.vue";
import Settings from "@/components/Settings/Settings.vue";
import ChangePassword from "@/components/Settings/ChangePassword.vue";
import EditProfile from "@/components/Settings/EditProfile.vue";
import ResetPassword from "@/components/Auth/ResetPassword.vue";
import ConfirmResetPassword from "@/components/Auth/ConfirmResetPassword.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/auth', component: AuthPage},
        {path: '/reset-password', component: ResetPassword},
        {path: '/confirm-reset-password', component: ConfirmResetPassword},
        {
            path: '/', component: HomeView, children: [
                {path: '', component: HomePage},
                {path: 'search', component: Search},
                {path: 'chat', component: Chat},
                {path: 'notifications', component: Notifications},
                {path: 'profile', component: Profile},
            ]
        },
        {path: '/settings', component: Settings},
        {path: '/change-password', component: ChangePassword},
        {path: '/edit-profile', component: EditProfile},
    ]
});

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token');
    if (to.path === '/reset-password' || to.path === '/confirm-reset-password') {
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
