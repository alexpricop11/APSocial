<template>
  <div class="container">
    <div class="top-bar">
      <button @click="goBack" class="back-button">
        <span class="material-icons">arrow_back</span> Înapoi
      </button>
      <h1 class="title">Editează profilul</h1>
    </div>
    <div class="edit-profile-container">
      <form @submit.prevent="editProfile">
        <div>
          <label for="username">Username</label>
          <input type="text" id="username" v-model="profileData.username"/>
        </div>

        <div>
          <label for="email">Email</label>
          <input type="email" id="email" v-model="profileData.email"/>
        </div>

        <div>
          <label for="phone_number">Număr de telefon</label>
          <input type="text" id="phone_number" v-model="profileData.phone_number"/>
        </div>

        <div>
          <label for="birthday">Data nașterii</label>
          <input type="date" id="birthday" v-model="profileData.birthday"/>
        </div>

        <button type="submit">Salvează modificările</button>

        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      </form>
    </div>
  </div>
</template>

<script>
import apiClient from "@/services/api.js";
import router from "@/router/routing.js";

export default {
  data() {
    return {
      profileData: {
        username: "",
        email: "",
        phone_number: "",
        birthday: "",
      },
      errorMessage: "",
      successMessage: "",
    };
  },
  created() {
    this.fetchProfileData();
  },
  methods: {
    async fetchProfileData() {
      try {
        const response = await apiClient.get("/profile");
        this.profileData = response.data;
      } catch (error) {
        console.error("Eroare la obținerea datelor profilului:", error);
        this.errorMessage = "Nu am putut încărca datele profilului.";
      }
    },
    async editProfile() {
      try {
        await apiClient.post("/edit-profile", this.profileData);
        this.successMessage = "Profilul a fost actualizat cu succes!";
        this.errorMessage = "";
      } catch (error) {
        console.error("Eroare la actualizarea profilului:", error);
        this.errorMessage = "A apărut o eroare. Te rugăm să încerci din nou.";
        this.successMessage = "";
      }
    },
  goBack() {
    router.back();
  }
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  flex-direction: column;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  background-color: #1a1a1a;
  padding: 12px 20px;
  color: white;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}

.title {
  font-size: 1.6rem;
  font-weight: bold;
  text-align: center;
  flex-grow: 1;
  margin-left: 10px;
  color: white;
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

.edit-profile-container {
  margin-top: 80px;
  width: 100%;
  max-width: 480px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 1.8rem;
  text-align: center;
  color: #ffffff;
}


label {
  display: block;
  font-size: 1rem;
  color: #ffffff;
  margin-bottom: 6px;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  color: #333;
  background-color: #f8f8f8;
  transition: border-color 0.3s ease, background-color 0.3s ease;
}

input:focus {
  border-color: #4CAF50;
  background-color: #fff;
  outline: none;
}

button {
  background-color: #4CAF50;
  margin-top: 0.5rem;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}


.error-message, .success-message {
  text-align: center;
  margin-top: 20px;
  padding: 10px;
  border-radius: 4px;
  font-size: 1rem;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
}
</style>