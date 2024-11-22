<template>
  <div class="auth-page">
    <div class="auth-buttons">
      <button @click="showForm('register')" :class="{ active: activeForm === 'register' }">Înregistrare</button>
      <button @click="showForm('login')" :class="{ active: activeForm === 'login' }">Logare</button>
    </div>
    <div class="auth-form">
      <RegisterForm v-if="activeForm === 'register'" />
      <LoginForm v-if="activeForm === 'login'" />
    </div>
  </div>
</template>

<script>
import LoginForm from './LoginForm.vue';
import RegisterForm from './RegisterForm.vue';

export default {
  components: { LoginForm, RegisterForm },
  data() {
    return {
      activeForm: 'register',
    };
  },
  methods: {
    showForm(form) {
      this.activeForm = form;
    },
  },
};
</script>

<style scoped>
.auth-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #070606;
  color: rgba(60, 56, 56, 0);
}

.auth-buttons {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.auth-buttons button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #ffffff;
  color: #070606;
  transition: background-color 0.3s;
}

.auth-buttons button:hover {
  background-color: #1ae11a;
}

.auth-buttons .active {
  background-color: #1ae11a;
}

.auth-form {
  width: 100%;
  max-width: 400px;
  background-color: rgb(255, 255, 255);
  border-radius: 8px;
  padding: 20px;
  color: black;
}
</style>
