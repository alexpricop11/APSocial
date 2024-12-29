<template>
  <div class="container">
    <div class="top-bar">
      <button @click="goBack" class="back-button">
        <span class="material-icons">arrow_back</span> Înapoi
      </button>
      <h1 class="title">Setări</h1>
    </div>
    <div class="settings-list-container">
      <ul class="settings-list">
        <li @click="handleMenuAction('changePassword')">Schimbă Parola</li>
        <li @click="handleMenuAction('editProfile')">Editează Profilul</li>
        <li @click="handleMenuAction('changeProfileImage')">Schimbă Imaginea de Profil</li>
        <li @click="handleMenuAction('logout')">Iesire</li>
      </ul>
    </div>
  </div>
</template>

<script>
import {useRouter} from "vue-router";

export default {
  setup() {
    const router = useRouter();

    const handleMenuAction = (action) => {
      switch (action) {
        case "changePassword":
          router.push("/change-password");
          break;
        case "editProfile":
          router.push('/edit-profile')
          break;
        case "logout":
          router.push("/auth");
          localStorage.removeItem('token');
          break;
        default:
          console.log(`Unknown action: ${action}`);
      }
    };

    const goBack = () => {
      router.push('/profile');
    };

    return {
      handleMenuAction,
      goBack,
    };
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
  padding: 10px 20px;
  color: white;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  flex-grow: 1;
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

.settings-list-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 1rem;
  padding-top: 0;
  width: 100%;
}

.settings-list {
  list-style: none;
  padding: 0;
  color: white;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.settings-list li {
  font-size: 1.5rem;
  padding: 0.5rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.settings-list li:hover {
  background: #1ae11a;
  color: white;
}
</style>
