<template>
  <div class="profile-image-container">
    <div class="image-preview" v-if="imagePreview || currentImage">
      <img :src="imagePreview || currentImage" alt="Profile" class="preview-img"/>
    </div>

    <div class="upload-controls">
      <label class="upload-button">
        <input
            type="file"
            @change="handleImageSelect"
            accept="image/*"
            class="hidden"
        />
        Select Image
      </label>

      <button
          @click="uploadImage"
          :disabled="!selectedFile"
          class="upload-submit"
          :class="{ 'loading': isUploading }"
      >
        {{ isUploading ? 'Uploading...' : 'Upload Image' }}
      </button>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
import {ref} from 'vue'
import apiClient from "@/services/api.js";
import router from "@/router/routing.js";

export default {
  name: 'ProfileImage',
  props: {
    currentImage: {
      type: String,
      default: ''
    }
  },

  setup(props, {emit}) {
    const selectedFile = ref(null)
    const imagePreview = ref('')
    const error = ref('')
    const isUploading = ref(false)

    const handleImageSelect = (event) => {
      const file = event.target.files[0]
      if (!file) return

      // Validare
      if (!file.type.includes('image/')) {
        error.value = 'Please select an image file'
        return
      }

      if (file.size > 5 * 1024 * 1024) { // 5MB
        error.value = 'Image must be less than 5MB'
        return
      }

      selectedFile.value = file
      error.value = ''

      // Creare preview
      const reader = new FileReader()
      reader.onload = (e) => {
        imagePreview.value = e.target.result
      }
      reader.readAsDataURL(file)
    }

    const uploadImage = async () => {
      if (!selectedFile.value) return

      const formData = new FormData()
      formData.append('image', selectedFile.value)

      isUploading.value = true
      error.value = ''

      try {
        const response = await apiClient.post('/user/profile/image', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        await router.push('/profile')
        emit('upload-success', response.data)
      } catch (err) {
        error.value = err.response?.data?.detail || 'Failed to upload image'
      } finally {
        isUploading.value = false
      }
    }

    return {
      selectedFile,
      imagePreview,
      error,
      isUploading,
      handleImageSelect,
      uploadImage
    }
  }
}
</script>

<style scoped>
.profile-image-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.image-preview {
  width: 200px;
  height: 200px;
  margin: 0 auto 20px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #ddd;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-controls {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 15px;
}

.upload-button {
  padding: 8px 16px;
  background-color: #4a5568;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.upload-submit {
  padding: 8px 16px;
  background-color: #4299e1;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.upload-submit:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.upload-submit.loading {
  opacity: 0.7;
}

.hidden {
  display: none;
}

.error-message {
  color: #e53e3e;
  text-align: center;
  margin-top: 10px;
}
</style>