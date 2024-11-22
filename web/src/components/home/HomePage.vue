<template>
  <div class="app-container">
    <!-- Sidebar global -->
    <SideBar />
  </div>
</template>

<script setup>
import SideBar from "@/components/home/SideBar.vue";
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
}
</style>
