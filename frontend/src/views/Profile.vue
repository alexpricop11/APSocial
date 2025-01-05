<template>
  <div class="flex items-center justify-between p-4 rounded-lg text-white">
    <div class="flex justify-center items-center">
      <div class="w-20 h-20 rounded-full overflow-hidden flex justify-center items-center">
        <img
          v-if="profile && profile.profile_image"
          :src="profile.profile_image"
          alt="Profile Image"
          class="w-full h-full object-cover rounded-full cursor-pointer"
          @click="showModal = true"
        />
        <span v-else class="material-icons text-6xl text-white">person</span>
      </div>
    </div>

    <!-- User Info Section -->
    <div class="flex-1 text-center mx-4">
      <div class="text-3xl font-bold">{{ profile ? profile.username : '' }}</div>
    </div>

    <!-- Settings Icon Section -->
    <div class="flex top-10 right-4 cursor-pointer">
      <router-link to="/settings">
        <span class="material-icons text-xl text-white">settings</span>
      </router-link>
    </div>

    <!-- Modal Overlay -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-70 flex justify-center items-center z-50" @click="showModal = false">
      <div class="relative max-w-full max-h-full bg-white rounded-lg" @click.stop>
        <img
          :src="profile.profile_image"
          alt="Profile Image"
          class="w-full h-auto object-contain rounded-lg"
        />
      </div>
    </div>
    <div class="">
      <Posts/>
    </div>
  </div>
</template>

<script>
import apiClient from "@/services/api.js";
import Posts from "@/components/Profile/Posts.vue";

export default {
  data() {
    return {
      profile: null,
      showModal: false,
    };
  },
  components: {
    Posts
  },
  created() {
    this.getProfile();
  },
  methods: {
    async getProfile() {
      try {
        const response = await apiClient.get('/profile');
        this.profile = response.data.profile;
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
