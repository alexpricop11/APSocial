<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <div>
        <label>Username:</label>
        <input v-model="formData.username" type="text" required />
      </div>
      <div>
        <label>Password:</label>
        <input v-model="formData.password" type="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      formData: {
        username: '',
        password: '',
      },
      message: '',
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post('/api/login', this.formData);
        this.$router.push('/home');
        this.message = response.data.message;
        localStorage.setItem('token', response.data.token);
      } catch (error) {
        this.message = error.response?.data?.error || 'An error occurred.';
      }
    },
  },
};
</script>
