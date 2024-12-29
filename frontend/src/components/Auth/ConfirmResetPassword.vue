<script setup>
import {ref} from 'vue';
import apiClient from "@/services/api.js";
import router from "@/router/routing.js";

const email = ref('');
const resetCode = ref('');
const newPassword = ref('');
const successMessage = ref('');
const errorMessage = ref('');

const confirmResetPassword = async () => {
  try {
    await apiClient.post("/auth/confirm-reset-password", {
      email: email.value,
      reset_code: resetCode.value,
      new_password: newPassword.value,
    });
    successMessage.value = "Parola a fost resetată cu succes!";
    errorMessage.value = '';
    await router.push('/auth')
  } catch (error) {
    errorMessage.value = "Codul este incorect sau a expirat.";
    successMessage.value = '';
  }
};
</script>

<template>
  <div class="reset-password-confirm-container">
    <form @submit.prevent="confirmResetPassword">
      <div>
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required/>
      </div>
      <div>
        <label for="resetCode">Cod de resetare</label>
        <input type="text" id="resetCode" v-model="resetCode" required/>
      </div>
      <div>
        <label for="newPassword">Parola nouă</label>
        <input type="password" id="newPassword" v-model="newPassword" required/>
      </div>
      <button type="submit">Resetare Parolă</button>
    </form>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<style scoped>
.reset-password-confirm-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

label {
  color: white;
  font-size: 1rem;
  margin-bottom: 5px;
  display: block;
}

form {
  display: flex;
  flex-direction: column;
  width: 300px;
}

input {
  padding: 10px;
  margin: 10px 0;
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
