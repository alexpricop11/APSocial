<template>
  <div class="profile-container">
    <div v-if="profile" class="profile-card">
      <img :src="profile.profile_image" alt="Profile Image" v-if="profile.profile_image" class="profile-image"/>
      <p class="profile-item"><strong>Username:</strong> {{ profile.username }}</p>
      <p class="profile-item"><strong>Email:</strong> {{ profile.email }}</p>
      <p class="profile-item"><strong>Phone Number:</strong> {{ profile.phone_number }}</p>
    </div>
    <div v-else class="loading-text">
      <p>Loading profile...</p>
    </div>
  </div>
</template>

<script>
import apiClient from "@/services/api.js";

export default {
  data() {
    return {
      profile: null
    };
  },
  created() {
    this.getProfile();
  },
  methods: {
    async getProfile() {
      try {
        const response = await apiClient.get('/profile');
        this.profile = await response.data;
      } catch (error) {
        console.error(error);
      }
    },
  },
}
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  margin-top: 20px;
}

.profile-card {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
  text-align: center;
}

.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 15px;
}

.profile-item {
  font-size: 16px;
  color: #333;
  margin: 10px 0;
}

.loading-text {
  font-size: 18px;
  color: #666;
}
</style>
