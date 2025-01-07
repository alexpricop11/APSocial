<template>
  <div class="flex flex-col items-center p-4 rounded-lg text-white flex-wrap">
    <!-- Profile Image and Username Section -->
    <div class="flex items-center w-full justify-center">
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

      <!-- User Info Section -->
      <div class="text-center ml-4">
        <div class="text-3xl font-bold">{{ profile ? profile.username : '' }}</div>
      </div>

      <!-- Settings Icon Section -->
      <div class="flex cursor-pointer ml-4">
        <router-link to="/settings">
          <span class="material-icons text-3xl text-white">settings</span>
        </router-link>
      </div>
    </div>

    <!-- Followers and Following Section -->
    <div class="text-white flex space-x-4 mt-4">
      <div>
        <span class="block text-lg font-bold text-center">{{ profile ? profile.posts_count : 0 }}</span>
        <span class="text-sm">Postări</span>
      </div>
      <div @click="fetchFollowers" class="cursor-pointer">
        <span class="block text-lg font-bold text-center">{{ profile ? profile.followers_count : 0 }}</span>
        <span class="text-sm">Urmăritori</span>
      </div>
      <div @click="fetchFollowing" class="cursor-pointer">
        <span class="block text-lg font-bold text-center">{{ profile ? profile.following_count : 0 }}</span>
        <span class="text-sm">Urmărești</span>
      </div>
    </div>

    <!-- Modal Overlay -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-70 flex justify-center items-center z-50"
         @click="showModal = false">
      <div class="relative max-w-full max-h-full bg-white rounded-lg" @click.stop>
        <img
          :src="profile.profile_image"
          alt="Profile Image"
          class="w-full h-auto object-contain rounded-lg"
        />
      </div>
    </div>

    <!-- Followers List Modal -->
    <FollowersList v-if="showFollowers" :followers="followers" @close="showFollowers = false"/>

    <!-- Following List Modal -->
    <FollowingList v-if="showFollowing" :following="following" @close="showFollowing = false"/>

    <!-- Posts Section -->
    <div class="mt-4 w-full">
      <Posts :profile="profile"/>
    </div>
  </div>
</template>

<script>
import apiClient from "@/services/api.js";
import Posts from "@/components/Profile/Posts.vue";
import FollowersList from "@/components/Profile/FollowersList.vue";
import FollowingList from "@/components/Profile/FollowingList.vue";

export default {
  data() {
    return {
      profile: null,
      showModal: false,
      showFollowers: false,
      showFollowing: false,
      followers: [],
      following: []
    };
  },
  components: {
    Posts,
    FollowersList,
    FollowingList
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
    async fetchFollowers() {
      try {
        const response = await apiClient.get('/followers');
        this.followers = response.data.followers;
        this.showFollowers = true;
      } catch (error) {
        console.error(error);
      }
    },
    async fetchFollowing() {
      try {
        const response = await apiClient.get('/following');
        this.following = response.data.following;
        this.showFollowing = true;
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
</style>