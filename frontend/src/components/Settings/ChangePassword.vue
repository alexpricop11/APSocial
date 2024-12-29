<template>
  <div class="container">
    <div class="top-bar">
      <button @click="goBack" class="back-button">
        <span class="material-icons">arrow_back</span> Înapoi
      </button>
      <h1 class="title">Resetează Parola</h1>
    </div>

    <form @submit.prevent="changePassword">
      <div>
        <label for="current_password">Parola curentă:</label>
        <input
            id="current_password"
            type="password"
            v-model="form.current_password"
            placeholder="Introduceti parola curentă"
        />
      </div>
      <div>
        <label for="new_password">Parola nouă:</label>
        <input
            id="new_password"
            type="password"
            v-model="form.new_password"
            placeholder="Introduceti parola nouă"
        />
      </div>
      <button type="submit">Schimbă Parola</button>
    </form>

    <!-- Mesajul de succes sau eroare -->
    <div v-if="message" class="message">
      <p>{{ message }}</p>
    </div>
  </div>
</template>

<script>
import apiClient from "@/services/api.js";
import {ref} from "vue";
import {useRouter} from "vue-router";

export default {
  setup() {
    const router = useRouter();
    const form = ref({
      current_password: '',
      new_password: ''
    });
    const message = ref('');

    const changePassword = async () => {
      try {
        const response = await apiClient.put("/change-password", form.value);
        if (response.status === 200) {
          message.value = "Parola a fost schimbată cu succes!";
        } else {
          message.value = "A apărut o problemă. Încercați din nou.";
        }
      } catch (error) {
        message.value = "Eroare la schimbarea parolei. Verificați datele introduse."; // Mesaj în caz de eroare
      }
    };

    const goBack = () => {
      router.back();
    };

    return {
      form,
      message,
      changePassword,
      goBack,
    };
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  background-color: #1a1a1a;
  padding: 10px 20px;
  color: white;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}

.back-button {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.back-button .material-icons {
  margin-right: 8px;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  flex-grow: 1;
  text-align: center;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #121212;
  flex-direction: column;
}

form {
  background-color: #2a2a2a;
  padding: 20px;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
}

label {
  color: white;
  font-size: 1rem;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #333;
  color: white;
  font-size: 1rem;
}

input::placeholder {
  color: #888;
}

button {
  background-color: #1ae11a;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #14b114;
}

p {
  margin-top: 1rem;
  font-weight: bold;
  color: #4caf50;
  text-align: center;
}
</style>
