<script>
import apiClient from "@/services/api.js";

export default {
  data() {
    return {
      selectedFile: null,
      posts: []
    };
  },
  created() {
    this.getPosts();
  },
  methods: {
    async getPosts() {
      try {
        const posts = await apiClient.get('/posts');
        this.posts = posts.data;
      } catch (error) {
        console.error(error);
      }
    },
    handleFileSelect(event) {
      this.selectedFile = event.target.files[0];
    },

    // Încarcă imaginea către backend
    async uploadImage() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append("image", this.selectedFile);

      try {
        const response = await apiClient.post("/create-post", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        this.posts.push(response.data); // Adaugă noua postare în listă
        this.selectedFile = null;
      } catch (error) {
        console.error("Failed to upload image:", error);
      }
    },
    getImageUrl(imagePath) {
      return `http://127.0.0.1:8000/${imagePath}`;
    },
  }
}
</script>

<template>
  <div>
    <!-- Formular pentru încărcarea imaginilor -->
    <div class="upload-section">
      <input type="file" @change="handleFileSelect" accept="image/*"/>
      <button @click="uploadImage" :disabled="!selectedFile">Încarcă imaginea</button>
    </div>

    <!-- Afișarea imaginilor încărcate -->
    <div class="gallery">
      <div v-for="post in posts" :key="post.id" class="gallery-item">
        <img :src="getImageUrl(post.image)" alt="Gallery Image" class="gallery-image"/>
      </div>
    </div>
  </div>
</template>

<style scoped>
.upload-section {
  margin-bottom: 20px;
  color: white;
}

.gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.gallery-item {
  position: relative;
  width: 150px;
  height: 150px;
  overflow: hidden;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.gallery-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

</style>