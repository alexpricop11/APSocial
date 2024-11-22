<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const profileData = ref(null);
const error = ref(null);

// Funcție pentru a încărca datele de profil
const fetchProfile = async () => {
  try {
    const response = await axios.get('/api/profile', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`, // Token-ul JWT
      },
    });
    profileData.value = response.data;
  } catch (err) {
    error.value = err.response?.data || 'Failed to fetch profile data';
  }
};

onMounted(fetchProfile);
</script>

<template>
  <div class="profile-container">
    <!-- Mesaj de eroare -->
    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <!-- Datele profilului -->
    <div v-else-if="profileData" class="profile-card">
      <div class="profile-header">
        <img :src="profileData.profile_image" alt="Profile Image" />
        <h2 class="username">{{ profileData.username }}</h2>
      </div>

      <div class="profile-info">
        <p><strong>Email:</strong> {{ profileData.email }}</p>
        <p><strong>Data nașterii:</strong> {{ profileData.birthday }}</p>
        <p><strong>Online:</strong> {{ profileData.online ? 'Da' : 'Nu' }}</p>
        <p><strong>Urmăritori:</strong> {{ profileData.followers_count }}</p>
        <p><strong>Urmăriți:</strong> {{ profileData.following_count }}</p>
      </div>

      <div class="profile-lists">
        <div class="list">
          <h3>Urmăritori:</h3>
          <ul>
            <li v-for="follower in profileData.followers" :key="follower">{{ follower }}</li>
          </ul>
        </div>

        <div class="list">
          <h3>Urmăriți:</h3>
          <ul>
            <li v-for="following in profileData.following" :key="following">{{ following }}</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Încărcare -->
    <div v-else class="loading">
      <p>Se încarcă...</p>
    </div>
  </div>
</template>

<style scoped>
/* Container general */
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  color: white;
  background-color: #121212;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Card de profil */
.profile-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Header-ul profilului */
.profile-header {
  text-align: center;
  margin-bottom: 20px;
}

img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 2px solid #f2f2f2;
}

.username {
  font-size: 1.8em;
  margin-top: 10px;
  color: #f2f2f2;
}

/* Informații de profil */
.profile-info {
  background-color: #1e1e1e;
  padding: 15px;
  width: 100%;
  border-radius: 10px;
  margin-bottom: 20px;
}

.profile-info p {
  margin: 5px 0;
  font-size: 1em;
}

/* Listele */
.profile-lists {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
}

.list {
  flex: 1;
  background-color: #1e1e1e;
  padding: 10px;
  border-radius: 10px;
}

h3 {
  margin-bottom: 10px;
  font-size: 1.2em;
  border-bottom: 1px solid #444;
  padding-bottom: 5px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin: 5px 0;
  font-size: 0.9em;
}

/* Mesaj de eroare */
.error {
  color: red;
  text-align: center;
  font-weight: bold;
  background: #2e2e2e;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 20px;
}

/* Încărcare */
.loading {
  text-align: center;
  font-size: 1.2em;
  color: #f2f2f2;
}
</style>
