<template>
  <div class="auth-container">
    <h1>Bun venit pe AP Social!</h1>

    <div class="tab-buttons">
      <button :class="{ active: isRegisterActive }" @click="isRegisterActive = true">Înregistrare</button>
      <button :class="{ active: !isRegisterActive }" @click="isRegisterActive = false">Login</button>
    </div>

    <Register v-if="isRegisterActive"/>
    <Login v-else/>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import Login from "@/components/Auth/Login.vue";
import Register from "@/components/Auth/Register.vue";

const isRegisterActive = ref(true)
</script>

<style scoped>
.auth-container {
  max-width: 450px;
  margin: 0 auto;
  padding: 3rem;
  background-color: #111827;
  border-radius: 1rem;
  color: white;
}

h1 {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: #22ec22;
}

.tab-buttons {
  display: flex;
  margin-bottom: 1.5rem;
  color: #1ae11a;
}

.tab-buttons button {
  flex: 1;
  padding: 0.5rem;
  font-size: 1rem;
  background-color: #374151;
  border: none;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.tab-buttons button:first-child {
  border-radius: 0.375rem 0 0 0.375rem;
}

.tab-buttons button:last-child {
  border-radius: 0 0.375rem 0.375rem 0;
}

.tab-buttons button.active {
  background-color: #1ae11a;
}
</style>


