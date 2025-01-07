<template>
  <div class="min-h-screen flex flex-col items-center">
    <!-- Top Bar -->
    <div class="w-full bg-gray-800 text-white fixed top-0 left-0 py-3 px-4 flex items-center justify-between shadow-md">
      <button @click="goBack" class="flex items-center text-white hover:text-gray-300">
        <span class="material-icons">arrow_back</span>
        <span class="ml-2">Înapoi</span>
      </button>
    </div>

    <!-- Edit Profile Form -->
    <div class="mt-12 w-full max-w-md bg-gray-800 rounded-lg shadow-md p-5 mb-20">
      <form @submit.prevent="editProfile">
        <!-- Profile Image -->
        <div class="text-center mb-6">
          <div class="w-32 h-32 mx-auto rounded-full overflow-hidden border-4 border-green-500">
            <img
                :src="imagePreview || profileData.profile_image || 'https://via.placeholder.com/150'"
                alt="Profile"
                class="w-full h-full object-cover"
            />
          </div>
          <label class="mt-4 inline-block bg-blue-500 text-white px-4 py-2 rounded-lg cursor-pointer hover:bg-blue-600">
            <input type="file" @change="handleImageSelect" accept="image/*" class="hidden"/>
            Selectează imaginea
          </label>
        </div>

        <!-- Username -->
        <div class="mb-4">
          <label for="username" class="block text-white font-medium mb-2">Username</label>
          <input
              type="text"
              id="username"
              v-model="profileData.username"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-black"
          />
        </div>

        <!-- Email -->
        <div class="mb-4">
          <label for="email" class="block text-white font-medium mb-2">Email</label>
          <input
              type="email"
              id="email"
              v-model="profileData.email"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-black"
          />
        </div>

        <!-- Phone Number -->
        <div class="mb-4">
          <label for="phone_number" class="block text-white font-medium mb-2">Număr de telefon</label>
          <input
              type="text"
              id="phone_number"
              v-model="profileData.phone_number"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-black"
          />
        </div>

        <!-- Birthday -->
        <div class="mb-4">
          <label for="birthday" class="block text-white font-medium mb-2">Data nașterii</label>
          <input
              type="date"
              id="birthday"
              v-model="profileData.birthday"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-black"
          />
        </div>

        <!-- Bio -->
        <div class="mb-6">
          <label for="bio" class="block text-white font-medium mb-2">Bio</label>
          <textarea
              id="bio"
              v-model="profileData.bio"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-black"
          ></textarea>
        </div>

        <!-- Submit Button -->
        <button
            type="submit"
            class="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition duration-300"
        >
          Salvează modificările
        </button>

        <!-- Error and Success Messages -->
        <div v-if="errorMessage" class="mt-4 text-center text-red-600 bg-red-100 px-4 py-2 rounded-lg">
          {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="mt-4 text-center text-green-600 bg-green-100 px-4 py-2 rounded-lg">
          {{ successMessage }}
        </div>
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
        profile_image: "",
        username: "",
        email: "",
        phone_number: "",
        birthday: "",
        bio: "",
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
        this.profileData = response.data.profile;
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
          bio: this.profileData.bio,
        };

        const response = await apiClient.post("/edit-profile", profileData);

        if (response.data.new_token) {
          localStorage.setItem('token', response.data.new_token);
        }

        if (this.selectedFile) {
          const imageFormData = new FormData();
          imageFormData.append("image", this.selectedFile);

          await apiClient.post("/user/profile/image", imageFormData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });
        }

        this.successMessage = "Profilul a fost actualizat cu succes!";
        await this.fetchProfileData();
        await router.push('/profile');
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
</style>