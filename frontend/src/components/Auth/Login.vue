<template>
  <form @submit.prevent="loginUser" class="space-y-4">
    <div class="relative">
      <input type="text" v-model="form.username" placeholder="Numele" required
             class="w-full p-3 bg-gray-900 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-gray-500">
      <div v-if="errors.username" class="text-red-500 text-sm mt-1">{{ errors.username }}</div>
    </div>

    <div class="relative">
      <input :type="showPassword ? 'text' : 'password'" v-model="form.password" placeholder="Parola" required
             class="w-full p-3 bg-gray-900 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-gray-500">
      <button type="button" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400"
              @click="showPassword = !showPassword">
        <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
      </button>
      <div v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password }}</div>
    </div>

    <div class="text-right mb-2">
      <button type="button" class="text-green-500 hover:underline" @click="goToResetPassword">Ai uitat parola?</button>
    </div>

    <button type="submit"
            class="w-full p-3 bg-green-500 rounded-md text-white font-semibold hover:bg-green-600 transition-colors">
      Login
    </button>

    <div v-if="generalError" class="text-red-500 text-sm mt-2">{{ generalError }}</div>
  </form>
</template>

<script setup>
import {ref} from 'vue';
import apiClient from "@/services/api.js";
import router from "@/router/routing.js";

const showPassword = ref(false);
const form = ref({
  username: '',
  password: ''
});
const errors = ref({});
const generalError = ref('');

const loginUser = async () => {
  errors.value = {};
  generalError.value = '';
  try {
    const response = await apiClient.post('/auth/login', form.value);
    localStorage.setItem('token', response.data.token);
    console.log(response);
    await router.push('/');
  } catch (error) {
    if (error.response && error.response.data) {
      if (error.response.data.detail) {
        generalError.value = error.response.data.detail;
      } else {
        errors.value = error.response.data;
      }
    } else if (error.message) {
      generalError.value = error.message;
    } else {
      generalError.value = 'A apărut o eroare necunoscută.';
    }
    console.error('Login error:', error);
  }
};

const goToResetPassword = () => {
  router.push('/reset-password');
};
</script>

<style scoped>
</style>