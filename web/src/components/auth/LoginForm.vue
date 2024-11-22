<template>
  <div class="login-container">
    <form @submit.prevent="loginUser" class="login-form">
      <div class="form-group">
        <label>Numele:</label>
        <input v-model="formData.username" type="text" required/>
      </div>
      <div class="form-group">
        <label>Parola:</label>
        <input v-model="formData.password" type="password" required/>
        <div class="forgot-password">
          <a @click="forgotPassword" href="#">Ai uitat parola?</a>
        </div>
      </div>
      <button type="submit" class="login-button">Login</button>
    </form>
    <p v-if="message" class="message">{{ message }}</p>
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
    forgotPassword() {
      this.$router.push('/forgot-password');
    },
  },
};
</script>

<style>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(60, 56, 56, 0);
}

h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.login-form {
  width: 100%;
  background-color: rgba(60, 56, 56, 0);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.3s ease;
}

input:focus {
  border-color: #070606;
}

.login-button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  background-color: #070606;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #1ae11a;
}

.message {
  margin-top: 10px;
  font-size: 14px;
  color: #333;
  text-align: center;
}

.forgot-password {
  margin-top: 5px;
  text-align: right;
}

.forgot-password a {
  font-size: 14px;
  color: #007bff;
  text-decoration: none;
  cursor: pointer;
  transition: color 0.3s ease;
}

.forgot-password a:hover {
  color: #0056b3;
}
</style>
