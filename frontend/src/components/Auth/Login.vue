<template>
  <form @submit.prevent="loginUser">
    <div class="form-group">
      <input type="text" v-model="form.username" placeholder="Numele" required>
    </div>

    <div class="form-group password-group">
      <input :type="showPassword ? 'text' : 'password'" v-model="form.password" placeholder="Parola" required>
      <button type="button" class="eye-button" @click="showPassword = !showPassword">👁</button>
    </div>

    <button type="submit" class="submit-button">Login</button>
  </form>
</template>

<script setup>
import {ref} from 'vue'
import apiClient from "@/services/api.js";
import router from "@/router/routing.js";

const showPassword = ref(false)
const form = ref({
  username: '',
  password: ''
})
const errors = ref({});

const loginUser = async () => {
  errors.value = {};
  try {
    const response = await apiClient.post('/auth/login', form.value);
    localStorage.setItem('token', response.data.token);
    await router.push('/')
  } catch (error) {
    if (error.response && error.response.data) {
      errors.value = error.response.data.detail;
    } else {
      console.error('Login error:', error);
    }
  }
};
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
  max-width: 95%;
  position: relative;
}

input {
  width: 100%;
  padding: 0.75rem;
  background-color: #111827;
  border: 1px solid #4B5563;
  border-radius: 0.375rem;
  color: white;
  font-size: 1rem;
}

input::placeholder {
  color: #9CA3AF;
}

input:focus {
  outline: none;
  border-color: #6B7280;
}

.password-group {
  position: relative;
}

.eye-button {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9CA3AF;
  cursor: pointer;
  padding: 0;
}

.submit-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #1ae11a;
  border: none;
  border-radius: 0.375rem;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

</style>