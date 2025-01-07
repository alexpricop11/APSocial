<template>
  <div class="p-4">
    <!-- Navigation Bar -->
    <div class="flex justify-between items-center mb-4">
      <button @click="goBack" class="flex items-center px-4 py-2 text-white rounded">
        <i class="fas fa-arrow-left mr-2"></i> Înapoi
      </button>
    </div>
    <!-- Loading State -->
    <div v-if="loading" class="text-center text-gray-500">
      <i class="fas fa-spinner fa-spin"></i> Se încarcă...
    </div>

    <!-- User Profile -->
    <div v-else-if="user" class="mt-4 flex flex-col items-center text-center">
      <div class="flex items-center justify-center w-full mb-4">
        <!-- Profile Image -->
        <div class="w-32 h-32 rounded-full bg-gray-200 flex items-center justify-center mr-4">
          <img
              v-if="user.profile_image"
              :src="user.profile_image"
              alt="Profile Image"
              class="w-full h-full rounded-full object-cover"
          />
          <i v-else class="fas fa-user text-6xl text-gray-500"></i>
        </div>

        <!-- Username and Follow/Unfollow Button -->
        <div class="flex flex-col items-start">
          <div class="flex items-center">
            <h1 class="text-3xl font-bold text-white mr-4">{{ user.username }}</h1>
            <button
                @click="toggleFollow"
                class="px-4 py-2 bg-blue-500 text-white rounded"
            >
              {{ isFollowing ? 'Ne urmărește' : 'Urmărește' }}
            </button>
          </div>

          <!-- Followers and Following -->
          <div class="flex space-x-4 mt-2">
            <div class="text-white">
              <i></i> Postări: {{ user.posts_count }}
            </div>
            <div class="text-white">
              <i class="fas fa-users"></i> Followers: {{ user.followers_count }}
            </div>
            <div class="text-white">
              <i class="fas fa-user-friends"></i> Following: {{ user.following_count }}
            </div>
          </div>
        </div>
      </div>

      <!-- Bio -->
      <p v-if="user.bio" class="text-white mt-4">{{ user.bio }}</p>
    </div>

    <div v-else class="text-center text-red-500">
      <i class="fas fa-exclamation-circle"></i> Nu s-a putut încărca profilul.
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import apiClient from "@/services/api.js";
import router from "@/router/routing.js";

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

    const goBack = () => {
      router.back();
    };

    onMounted(() => {
      fetchUserProfile();
    });

    return {
      user,
      loading,
      isFollowing,
      toggleFollow,
      goBack,
    };
  },
};
</script>

<style scoped>
</style>