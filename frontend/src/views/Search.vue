<template>
  <div class="p-4">
    <SearchBar @search="handleSearch"/>

    <div v-if="loading" class="mt-4 text-gray-500">Se încarcă...</div>
    <div v-else-if="searchResults.length" class="mt-4">
      <ul>
        <li v-for="result in searchResults" :key="result.id" class="mt-2 flex items-center">
          <img
              :src="result.profile_image"
              alt="Profile Image"
              class="w-20 h-20 rounded-full mr-3"
          />
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
      searchQuery: "", // Query-ul de căutare
      searchResults: [], // Rezultatele căutării
      loading: false, // Starea de încărcare
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
  },
};
</script>

<style scoped>
</style>