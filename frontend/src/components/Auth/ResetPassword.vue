<script setup>
import { ref } from 'vue';
import apiClient from "@/services/api.js";
import router from "@/router/routing.js";

const email = ref('');
const successMessage = ref('');
const errorMessage = ref('');

const requestResetPassword = async () => {
  try {
    await apiClient.post("/auth/reset-password", { email: email.value });
    successMessage.value = "Un cod a fost trimis pe emailul tău.";
    errorMessage.value = '';
    await router.push('/confirm-reset-password')
  } catch (error) {
    errorMessage.value = "Nu am putut trimite codul de resetare. Te rugăm să încerci din nou.";
    successMessage.value = '';
  }
};
</script>

<template>
  <div class="reset-password-container">
    <form @submit.prevent="requestResetPassword">
      <div>
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" placeholder="Email" required />
      </div>
      <button type="submit">Trimite codul de resetare</button>
    </form>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<style scoped>
.reset-password-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

h1 {
  margin-bottom: 20px;
  font-size: 1.5rem;
}

form {
  display: flex;
  flex-direction: column;
  width: 300px;
}

input {
  padding: 10px;
  margin: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button {
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.success-message {
  color: green;
  margin-top: 10px;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>
