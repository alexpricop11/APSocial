<template>
  <div class="container">
    <div class="top-bar">
      <button @click="goBack" class="back-button">
        <span class="material-icons">arrow_back</span> Înapoi
      </button>
      <h1 class="title">Editează profilul</h1>
    </div>
    <div class="edit-profile-container">
      <form @submit.prevent="editProfile">
        <div class="profile-image-container">
          <div class="image-preview" v-if="imagePreview || profileData.currentImage">
            <img :src="imagePreview || profileData.currentImage" alt="Profile" class="preview-img"/>
          </div>
          <label class="upload-button">
            <input
                type="file"
                @change="handleImageSelect"
                accept="image/*"
                class="hidden"
            />
            Selectează imaginea
          </label>
        </div>
        <div>
          <label for="username">Username</label>
          <input type="text" id="username" v-model="profileData.username"/>
        </div>

        <div>
          <label for="email">Email</label>
          <input type="email" id="email" v-model="profileData.email"/>
        </div>

        <div>
          <label for="phone_number">Număr de telefon</label>
          <input type="text" id="phone_number" v-model="profileData.phone_number"/>
        </div>

        <div>
          <label for="birthday">Data nașterii</label>
          <input type="date" id="birthday" v-model="profileData.birthday"/>
        </div>

        <button type="submit">Salvează modificările</button>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      </form>
    </div>
  </div>
</template>

<script>
import apiClient from "@/services/api.js";
import router from "@/router/routing.js";

export default {
  data() {
    return {
      profileData: {
        username: "",
        email: "",
        phone_number: "",
        birthday: "",
        currentImage: "",
      },
      selectedFile: null,
      imagePreview: "",
      errorMessage: "",
      successMessage: "",
      isUploading: false,
    };
  },
  created() {
    this.fetchProfileData();
  },
  methods: {
    async fetchProfileData() {
      try {
        const response = await apiClient.get("/profile");
        this.profileData = response.data;
      } catch (error) {
        this.errorMessage = "Nu am putut încărca datele profilului.";
      }
    },
    handleImageSelect(event) {
      const file = event.target.files[0];
      if (!file) return;

      if (!file.type.includes("image/")) {
        this.errorMessage = "Te rugăm să selectezi un fișier imagine.";
        return;
      }

      if (file.size > 5 * 1024 * 1024) {
        this.errorMessage = "Imaginea trebuie să fie mai mică de 5MB.";
        return;
      }

      this.selectedFile = file;
      this.errorMessage = "";

      const reader = new FileReader();
      reader.onload = (e) => {
        this.imagePreview = e.target.result;
      };
      reader.readAsDataURL(file);
    },

    async editProfile() {
      try {
        const profileData = {
          username: this.profileData.username,
          email: this.profileData.email,
          phone_number: this.profileData.phone_number,
          birthday: this.profileData.birthday,
        };

        await apiClient.post("/edit-profile", profileData);

        // Handle image upload separately
        if (this.selectedFile) {
          const imageFormData = new FormData();
          imageFormData.append("image", this.selectedFile); // Schimbă "file" în "image"

          await apiClient.post("/user/profile/image", imageFormData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });
        }

        this.successMessage = "Profilul a fost actualizat cu succes!";
        await this.fetchProfileData();
        await router.push('/profile')
      } catch (error) {
        this.errorMessage = "A apărut o eroare. Te rugăm să încerci din nou.";
        console.error(error);
      }
    },
    goBack() {
      router.back();
    }
  },
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  background-color: #1a1a1a;
  color: white;
  position: fixed;
  top: 0;
  left: 0;
  padding: 10px; /* Reducerea padding-ului general */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Adaugă o umbră pentru a evidenția bara */
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  color: white;
  margin: 0 auto;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.back-button {
  position: relative;
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  display: inline-flex; /* Schimbat din flex pentru a limita dimensiunea */
  align-items: center;
  padding: 10px; /* Adaugă padding pentru a mări zona de clic */
}

.back-button span.material-icons {
  margin-right: 5px; /* Margine între icon și text */
}


.edit-profile-container {
  margin-top: 80px;
  width: 100%;
  max-width: 480px;
  background-color: rgba(255, 255, 255, 0.04);
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 25px;
}

h1 {
  font-size: 2rem;
  text-align: center;
  color: #444;
  margin-bottom: 20px;
}

label {
  display: block;
  font-size: 1rem;
  color: #ffffff;
  margin-bottom: 8px;
  font-weight: 500;
}

input[type="text"],
input[type="email"],
input[type="tel"],
input[type="date"] {
  width: 90%;
  padding: 12px 15px;
  margin-bottom: 15px;
  color: #070606;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

input:focus {
  border-color: #4CAF50;
  background-color: #fdfdfd;
  outline: none;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.5);
}

button {
  width: 100%;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  padding: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-weight: bold;
}

button:hover {
  background-color: #45a049;
}

.profile-image-container {
  text-align: center;
  margin-bottom: 25px;
}

.image-preview {
  width: 120px;
  height: 120px;
  margin: 0 auto;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #4CAF50;
  position: relative;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}


.upload-button {
  padding: 10px 20px;
  background-color: #4299e1;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.upload-button:hover {
  background-color: #3182ce;
}

.error-message, .success-message {
  text-align: center;
  margin-top: 20px;
  padding: 10px;
  border-radius: 4px;
  font-size: 1rem;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
}

</style>