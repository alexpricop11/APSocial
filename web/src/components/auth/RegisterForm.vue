<template>
  <div class="register-container">
    <form @submit.prevent="registerUser" class="register-form">
      <div class="form-group">
        <label>Numele:</label>
        <input v-model="formData.username" type="text" required/>
      </div>
      <div class="form-group">
        <label>Parola:</label>
        <input v-model="formData.password" type="password" required/>
      </div>
      <div class="form-group">
        <label>Email:</label>
        <input v-model="formData.email" type="email"/>
      </div>
      <div class="form-group">
        <label>Numărul de telefon:</label>
        <input v-model="formData.phone_number" type="text"/>
      </div>
      <div class="form-group">
        <label>Ziua de naștere:</label>
        <input v-model="formData.birthday" type="date"/>
      </div>
      <button type="submit" class="register-button">Înregistrează</button>
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
        email: '',
        phone_number: '',
        birthday: '',
      },
      message: '',
    };
  },
  methods: {
    async registerUser() {
      const dataToSend = {...this.formData};
      if (!dataToSend.birthday) {
        delete dataToSend.birthday;
      }

      try {
        const response = await axios.post('/api/register', dataToSend);
        if (response.data.success) {
          localStorage.setItem('token', response.data.token);
          this.$router.push('/home');
        } else {
          this.message = response.data.message;
        }
      } catch (error) {
        this.message = error.response?.data || 'An error occurred.';
      }
    }
  }
}
</script>

<style scoped>
.register-container {
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

.register-form {
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

.register-button {
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

.register-button:hover {
  background-color: #1ae11a;
}

.message {
  margin-top: 10px;
  font-size: 14px;
  color: #333;
  text-align: center;
}
</style>
