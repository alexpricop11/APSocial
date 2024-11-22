import { createRouter, createWebHashHistory } from "vue-router";
import AuthPage from "@/components/auth/AuthPage.vue";
import Home from "@/components/home/Home.vue";
import Search from "@/components/search_bar/Search.vue";
import Chat from "@/components/chat/Chat.vue";
import Notification from "@/components/notification/Notification.vue";
import Profile from "@/components/profile/Profile.vue";

const routes = [
  { path: "/auth-page", component: AuthPage },
  { path: "/", component: Home, name: "Home" },
  { path: "/search", component: Search, name: "Search" },
  { path: "/chat", component: Chat, name: "Chat" },
  { path: "/notification", component: Notification, name: "Notification" },
  { path: "/profile", component: Profile, name: "Profile" },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
