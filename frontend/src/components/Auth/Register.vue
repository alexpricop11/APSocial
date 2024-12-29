<template>
  <form @submit.prevent="registerUser">
    <div class="form-group">
      <input type="text" v-model="form.username" placeholder="Numele" required>
    </div>

    <div class="form-group password-group">
      <input :type="showPassword ? 'text' : 'password'" v-model="form.password" placeholder="Parola" required>
      <button type="button" class="eye-button" @click="showPassword = !showPassword">👁</button>
    </div>
    <div class="form-group">
      <input type="email" v-model="form.email" placeholder="Email">
    </div>

    <div class="form-group">
      <input type="tel" v-model="form.phone" placeholder="Numărul de telefon">
    </div>

    <div class="form-group">
      <input type="date" v-model="form.birthday" placeholder="Data de naștere">
    </div>

    <button type="submit" class="submit-button">Înregistrează-te</button>
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
  color: #ffffff;
  cursor: pointer;
  padding: 0;
  font-size: 1.2rem;
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

