<template>
  <div class="profile-container">
    <div class="image-profile">
      <div class="profile-image-container">
        <img
            v-if="profile && profile.profile_image"
            :src="profile.profile_image"
            alt="Profile Image"
            class="profile-image"
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
  </div>
</template>


<script>
import apiClient from "@/services/api.js";

export default {
  components: {},
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
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

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
