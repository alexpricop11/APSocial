<script setup>
import {useRoute} from 'vue-router';
import NavBar from "@/components/nav_bar/NavBar.vue";

const route = useRoute();
</script>

<template>
  <div>
    <NavBar v-if="!route.meta.noNavBar"/>
    <div>
      <router-view/>
    </div>
  </div>
</template>


<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: black;
  color: white;
}
</style>
