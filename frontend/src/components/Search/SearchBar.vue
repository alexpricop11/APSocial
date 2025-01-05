<template>
  <div class="relative w-full max-w-md mx-auto">
    <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
      <svg
          class="h-5 w-5 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
      >
        <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
        ></path>
      </svg>
    </span>

    <input
        v-model="searchQuery"
        type="text"
        placeholder="Caută utilizatori..."
        class="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 bg-white text-gray-800 placeholder-gray-400"
        @input="handleInput"
    />
    <button
        @click="performSearch"
        class="absolute inset-y-0 right-0 px-6 py-3 bg-green-600 text-white rounded-r-full hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200"
    >
      Caută
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
    };
  },
  methods: {
    handleInput() {
      this.$emit("search", this.searchQuery);
    },
    performSearch() {
      this.$emit("search", this.searchQuery);
    },
  },
};
</script>

<style scoped>

</style>