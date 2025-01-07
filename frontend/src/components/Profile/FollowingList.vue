<template>
  <div class="fixed inset-0 bg-black bg-opacity-70 flex justify-center items-center z-50" @click="$emit('close')">
    <div class="bg-black rounded-lg p-6 max-w-lg w-full" @click.stop>
      <h2 class="text-2xl font-bold mb-4 text-center">Urmărești</h2>
      <ul class="space-y-4">
        <li v-for="following in following" :key="following.id" class="flex items-center space-x-4">
          <router-link :to="{ name: 'Profile', params: { id: following.id } }" class="flex items-center space-x-4">
            <div class="w-12 h-12 rounded-full overflow-hidden flex justify-center items-center bg-gray-200">
              <img v-if="following.profile_image" :src="following.profile_image" alt="Profile Image" class="w-full h-full object-cover">
              <span v-else class="material-icons text-gray-500">person</span>
            </div>
            <div>
              <div class="text-lg font-semibold">{{ following.username }}</div>
            </div>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    following: Array
  }
};
</script>

<style scoped>
</style>