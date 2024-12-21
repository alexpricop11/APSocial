<script setup>
import NavBar from "@/components/nav_bar/NavBar.vue";
</script>

<template>
  <div>
    <NavBar />
    <div class="home-content">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
</style>
