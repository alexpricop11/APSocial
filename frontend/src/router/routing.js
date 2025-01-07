import {createRouter, createWebHistory} from 'vue-router';
import AuthPage from "@/views/AuthPage.vue";
import HomePage from "@/views/HomePage.vue";
import Profile from "@/views/Profile.vue";
import Search from "@/views/Search.vue";
import Chat from "@/components/Chat.vue";
import Notifications from "@/components/Notifications.vue";
import Settings from "@/components/Settings/Settings.vue";
import ChangePassword from "@/components/Settings/ChangePassword.vue";
import EditProfile from "@/components/Settings/EditProfile.vue";
import ResetPassword from "@/components/Auth/ResetPassword.vue";
import ConfirmResetPassword from "@/components/Auth/ConfirmResetPassword.vue";
import OtherProfile from "@/views/OtherProfile.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/auth', component: AuthPage, meta: {noNavBar: true}},
        {path: '/reset-password', component: ResetPassword, meta: {noNavBar: true}},
        {path: '/confirm-reset-password', component: ConfirmResetPassword, meta: {noNavBar: true}},
        {path: '/', component: HomePage},
        {path: '/search', component: Search},
        {path: '/chat', component: Chat},
        {path: '/notifications', component: Notifications},
        {path: '/profile', component: Profile},
        {path: '/settings', component: Settings},
        {path: '/change-password', component: ChangePassword},
        {path: '/edit-profile', component: EditProfile},
        {
            path: '/profile/:id',
            name: "Profile",
            component: OtherProfile
        },
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
