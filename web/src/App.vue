<script setup>
import HomePage from "@/components/home/HomePage.vue";
</script>

<template>
  <div id="app">
    <HomePage />
  </div>
</template>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #070606;
}

#app {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #000;
}

</style>
