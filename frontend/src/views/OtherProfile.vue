<template>
  <div class="p-4">
    <!-- Loading State -->
    <div v-if="loading" class="text-center text-gray-500">
      <i class="fas fa-spinner fa-spin"></i> Se încarcă...
    </div>

    <!-- User Profile -->
    <div v-else-if="user" class="mt-4">
      <div class="flex flex-col items-center text-center">
        <!-- Profile Image or Icon -->
        <div class="w-32 h-32 rounded-full bg-gray-200 flex items-center justify-center mb-4">
          <img
              v-if="user.profile_image"
              :src="user.profile_image"
              alt="Profile Image"
              class="w-full h-full rounded-full object-cover"
          />
          <i v-else class="fas fa-user text-6xl text-gray-500"></i>
        </div>

        <!-- Username -->
        <h1 class="text-3xl font-bold text-white">{{ user.username }}</h1>

        <!-- Bio -->
        <p v-if="user.bio" class="text-white mt-2">{{ user.bio }}</p>

        <!-- Followers and Following -->
        <div class="flex space-x-4 mt-4">
          <div class="text-white">
            <i class="fas fa-users"></i> Followers: {{ user.followers_count }}
          </div>
          <div class="text-white">
            <i class="fas fa-user-friends"></i> Following: {{ user.following_count }}
          </div>
        </div>

        <!-- Follow/Unfollow Button -->
        <button
            @click="toggleFollow"
            class="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
        >
          {{ isFollowing ? 'Ne urmărește' : 'Urmărește' }}
        </button>
      </div>
    </div>

    <div v-else class="text-center text-red-500">
      <i class="fas fa-exclamation-circle"></i> Nu s-a putut încărca profilul.
    </div>
  </div>
</template>

<script>
import {ref, onMounted} from "vue";
import {useRoute} from "vue-router";
import apiClient from "@/services/api.js";

export default {
  setup() {
    const route = useRoute();
    const user = ref(null);
    const loading = ref(true);
    const isFollowing = ref(false);

    const fetchUserProfile = async () => {
      const userId = route.params.id;
      try {
        const response = await apiClient.get(`/profile/${userId}`);
        user.value = response.data;
        isFollowing.value = response.data.is_following;
      } catch (error) {
        console.error("Failed to fetch user profile:", error);
      } finally {
        loading.value = false;
      }
    };

    const toggleFollow = async () => {
      const userId = route.params.id;
      try {
        await apiClient.post(`/follow/${userId}`, {
          user_id: userId,
        });
        isFollowing.value = !isFollowing.value;
        if (isFollowing.value) {
          user.value.followers_count++;
        } else {
          user.value.followers_count--;
        }
      } catch (error) {
        console.error("Failed to follow/unfollow user:", error);
      }
    };

    onMounted(() => {
      fetchUserProfile();
    });

    return {
      user,
      loading,
      isFollowing,
      toggleFollow,
    };
  },
};
</script>

<style scoped>
</style>