<template>
  <div class="profile-container">
    <div class="image-profile">
      <div class="profile-image-container">
        <img
            v-if="profile && profile.profile_image"
            :src="profile.profile_image"
            alt="Profile Image"
            class="profile-image"
            @click="showModal = true"
        />
        <span v-else class="material-icons profile-icon">person</span>
      </div>
    </div>

    <div class="info-user">
      <div class="profile-username">{{ profile ? profile.username : '' }}</div>
      <div class="settings-icon-container">
        <router-link to="/settings">
          <span class="material-icons settings-icon">settings</span>
        </router-link>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click="showModal = false">
      <div class="modal-content" @click.stop>
        <img
            :src="profile.profile_image"
            alt="Profile Image"
            class="modal-image"
        />
      </div>
    </div>
  </div>
</template>
<script>

import apiClient from "@/services/api.js";

export default {
  data() {
    return {
      profile: null,
      showModal: false,
    };
  },
  created() {
    this.getProfile();
  },
  methods: {
    async getProfile() {
      try {
        const response = await apiClient.get('/profile');
        this.profile = response.data;
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  max-width: 100%;
  max-height: 100%;
  overflow: hidden;
  background: #fff;
  border-radius: 10px;
}

.modal-image {
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 10px;
}

.modal-overlay:hover {
  cursor: pointer;
}

.profile-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 10px;
  color: #ffffff;
  position: relative;
}

.image-profile {
  display: flex;
  justify-content: center;
  align-items: center;
}

.profile-image-container {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.profile-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.profile-icon {
  font-size: 48px;
  color: #ffffff;
}


.info-user {
  flex: 1;
  text-align: center;
  margin: 0 15px;
}

.profile-username {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 8px;
}

.profile-details p {
  font-size: 3rem;
  margin: 4px 0;
}

.settings-icon-container {
  position: fixed;
  top: 1.5rem;
  right: 1rem;
  cursor: pointer;
}

.settings-icon {
  font-size: 30px;
  color: #ffffff;
}

</style>
