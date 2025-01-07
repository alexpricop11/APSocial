<template>
  <div>
    <div class="mb-5 flex flex-col items-start gap-2">
      <input
          type="file"
          @change="handleFileSelect"
          accept="image/*"
          class="hidden"
          ref="fileInput"
          multiple
      />
      <button
          @click="handleUploadButtonClick"
          class="bg-blue-500 text-white px-4 py-2 p-5 rounded-lg hover:bg-blue-600 transition-colors"
      >
        Încarcă imagini in profil
      </button>
    </div>
    <div class="flex flex-wrap gap-4 pb-20 justify-center items-center">
      <div v-for="post in posts" :key="post.id"
           class="w-20 h-20 sm:w-24 sm:h-24 md:w-32 md:h-32 lg:w-40 lg:h-40 overflow-hidden rounded-lg border border-gray-300"
      >
        <img
            :src="getImageUrl(post.image)"
            alt="Gallery Image"
            class="w-full h-full object-cover"
        />
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from "@/services/api.js";

export default {
  props: {
    profile: Object
  },
  data() {
    return {
      selectedFiles: [],
      posts: [],
    };
  },
  created() {
    this.getPosts();
  },
  methods: {
    async getPosts() {
      try {
        const response = await apiClient.get('/get-posts');
        console.log("Postări încărcate:", response.data);
        this.posts = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    handleFileSelect(event) {
      const files = event.target.files;
      if (files.length > 0) {
        for (const file of files) {
          if (file.type.startsWith('image/')) {
            this.uploadImage(file);
          } else {
            alert("Te rugăm să selectezi doar fișiere de tip imagine.");
          }
        }
      } else {
        alert("Te rugăm să selectezi cel puțin un fișier.");
      }
    },
    handleUploadButtonClick() {
      this.$refs.fileInput.click();
    },
    async uploadImage(file) {
      const formData = new FormData();
      formData.append("image", file);

      try {
        const response = await apiClient.post("/create-post", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        this.posts.push(response.data.profile);
        this.profile.posts_count += 1;
        await this.getPosts();
      } catch (error) {
        alert("Încărcarea imaginii a eșuat. Te rugăm să încerci din nou.");
      }
    },
    getImageUrl(imagePath) {
      const baseUrl = "http://127.0.0.1:8000/static/";
      return `${baseUrl}${imagePath.split('/')[1]}`;
    },
  },
};
</script>