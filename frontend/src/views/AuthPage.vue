<template>
  <div class="max-w-lg mx-auto p-12 bg-gray-900 rounded-xl text-white shadow-lg">
    <h1 class="text-center mb-6 text-3xl font-bold text-green-500">Bun venit pe AP Social!</h1>

    <div class="flex mb-6">
      <button
          :class="['flex-1 p-3 text-lg font-semibold rounded-l-lg transition-colors duration-300', isRegisterActive ? 'bg-green-600 text-white' : 'bg-gray-700 hover:bg-gray-600']"
          @click="isRegisterActive = true">Înregistrare
      </button>
      <button
          :class="['flex-1 p-3 text-lg font-semibold rounded-r-lg transition-colors duration-300', !isRegisterActive ? 'bg-green-600 text-white' : 'bg-gray-700 hover:bg-gray-600']"
          @click="isRegisterActive = false">Login
      </button>
    </div>

    <Register v-if="isRegisterActive"/>
    <Login v-else/>
  </div>
</template>

<script setup>
import {ref} from 'vue';
import Login from '@/components/Auth/Login.vue';
import Register from '@/components/Auth/Register.vue';

const isRegisterActive = ref(true);
</script>

<style scoped>
</style>