<template>
  <form @submit.prevent="registerUser" class="space-y-4">
    <div class="relative">
      <input type="text" v-model="form.username" placeholder="Numele" required
             class="w-full p-3 bg-gray-900 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-gray-500">
    </div>

    <div class="relative">
      <input :type="showPassword ? 'text' : 'password'" v-model="form.password" placeholder="Parola" required
             class="w-full p-3 bg-gray-900 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-gray-500">
      <button type="button" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-white"
              @click="showPassword = !showPassword">
        <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
      </button>
    </div>
    <div class="relative">
      <input type="email" v-model="form.email" placeholder="Email"
             class="w-full p-3 bg-gray-900 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-gray-500">
    </div>

    <div class="relative">
      <input type="tel" v-model="form.phone" placeholder="Numărul de telefon"
             class="w-full p-3 bg-gray-900 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-gray-500">
    </div>

    <div class="relative">
      <input type="date" v-model="form.birthday"
             class="w-full p-3 bg-gray-900 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-gray-500">
    </div>

    <button type="submit"
            class="w-full p-3 bg-green-500 rounded-md text-white font-semibold hover:bg-green-600 transition-colors">
      Înregistrează-te
    </button>
  </form>
</template>

<script setup>
import {nextTick, ref} from 'vue'
import apiClient from "@/services/api.js";
import router from "@/router/routing.js";

const showPassword = ref(false)
const form = ref({
  username: null,
  password: null,
  email: null,
  phone: null,
  birthday: null
})
const errors = ref({});

const registerUser = async () => {
  errors.value = {};
  if (!form.value.email) {
    form.value.email = null;
  }
  try {
    const response = await apiClient.post('/auth/register', form.value);
    localStorage.setItem('token', response.data.token);
    await nextTick(() => {
      router.push('/');
    });
  } catch (error) {
    if (error.response && error.response.data) {
      errors.value = error.response.data.detail;
    } else {
      console.error('Registration error:', error);
    }
  }
};
</script>

<style scoped>
</style>