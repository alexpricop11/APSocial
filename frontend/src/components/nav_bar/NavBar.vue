<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
const menuItems = [
  { name: 'Acasă', icon: 'home', path: '/' },
  { name: 'Profil', icon: 'person', path: '/profile' },
];
</script>

<template>
  <div class="navigation-bar">
    <div
      v-for="(item, index) in menuItems"
      :key="index"
      class="nav-item"
      @click="router.push(item.path)"
    >
      <span class="material-icons">{{ item.icon }}</span>
      <span class="label">{{ item.name }}</span>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.navigation-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color: #070606;
  border-top: 1px solid #ddd;
  padding: 10px 0;
  z-index: 1000;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 14px;
  color: #ffffff;
  cursor: pointer;
  transition: color 0.3s;
}

.nav-item:hover {
  color: #1ae11a;
}

.material-icons {
  font-size: 24px;
}

.label {
  margin-top: 4px;
}
</style>
