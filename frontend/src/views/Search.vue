<template>
  <div class="p-4">
    <SearchBar @search="handleSearch"/>

    <div v-if="loading" class="mt-4 text-gray-500">Se încarcă...</div>
    <div v-else-if="searchResults.length" class="mt-4">
      <ul>
        <li
            v-for="result in searchResults"
            :key="result.id"
            class="mt-2 flex items-center cursor-pointer hover:bg-gray-800 p-2 rounded"
            @click="goToProfile(result.id)"
        >
          <img
              v-if="result.profile_image"
              :src="result.profile_image"
              alt="Profile Image"
              class="w-20 h-20 rounded-full mr-3"
          />
          <div v-else class="w-20 h-20 rounded-full mr-3 bg-black flex items-center justify-center">
            <span class="text-2xl">👤</span>
          </div>
          <span class="text-2xl">{{ result.username }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import SearchBar from "@/components/Search/SearchBar.vue";
import apiClient from "@/services/api.js";

export default {
  components: {
    SearchBar,
  },
  data() {
    return {
      searchQuery: "",
      searchResults: [],
      loading: false,
    };
  },
  methods: {
    async handleSearch(query) {
      this.searchQuery = query;
      if (query.trim() === "") {
        this.searchResults = [];
        return;
      }

      this.loading = true;
      try {
        console.log("Trimite cererea cu query:", query);
        const response = await apiClient.get("/search", {
          params: {query: query},
        });
        this.searchResults = response.data;
      } catch (error) {
        this.searchResults = [];
      } finally {
        this.loading = false;
      }
    },
    goToProfile(userId) {
      if (!userId) {
        console.error("User ID is missing or invalid.");
        return;
      }
      this.$router.push({name: "Profile", params: {id: userId}});
    },
  },
};
</script>

<style scoped>
</style>