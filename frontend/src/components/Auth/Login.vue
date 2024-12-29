<template>
  <form @submit.prevent="loginUser">
    <div class="form-group">
      <input type="text" v-model="form.username" placeholder="Numele" required>
      <div v-if="errors.username" class="error-message">{{ errors.username }}</div>
    </div>

    <div class="form-group password-group">
      <input :type="showPassword ? 'text' : 'password'" v-model="form.password" placeholder="Parola" required>
      <button type="button" class="eye-button" @click="showPassword = !showPassword">👁</button>
      <div v-if="errors.password" class="error-message">{{ errors.password }}</div>
    </div>

    <div class="reset-password">
      <button type="button" class="reset-link" @click="goToResetPassword">Ai uitat parola?</button>
    </div>

    <button type="submit" class="submit-button">Login</button>

    <!-- Afișăm mesajul de eroare global, dacă există -->
    <div v-if="generalError" class="error-message">{{ generalError }}</div>
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

.reset-password {
  margin-bottom: 0.5rem;
  text-align: end;
}

.reset-link {
  color: #ffffff;
  text-decoration: none;
  font-size: 1rem;
  background-color: green;
}

.reset-link:hover {
  text-decoration: underline;
}

/* Stilizarea pentru mesajele de eroare */
.error-message {
  color: red;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}
</style>
