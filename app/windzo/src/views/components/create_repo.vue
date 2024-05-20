<template>
  <div class="flex flex-col items-center justify-start min-h-screen bg-white py-6">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-8 max-w-lg w-full mt-4">
      <div class="flex justify-center mb-2">
        <!-- Placeholder for image/logo -->
        <img src="../../assets/logo/create_model.png" alt="Create Model" class="h-36 w-36">
      </div>
      <h2 class="text-2xl font-semibold text-center text-gray-900 dark:text-gray-200 mb-1">Create Model</h2>
      <p class="text-center text-gray-600 dark:text-gray-400 mb-4">
        A repository contains all model files, including the revision history.
      </p>
      <form @submit.prevent="createRepository" class="mt-4">
        <div class="mb-4">
          <label for="modelName" class="block text-gray-700 dark:text-gray-300 font-semibold mb-2">Model Name</label>
          <input type="text" id="modelName" v-model="modelName" required
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-gray-300">
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2">Visibility</label>
          <div class="border border-gray-300 dark:border-gray-700 rounded-lg">
            <div :class="{'bg-gray-200': visibility === 'public'}" class="flex items-center p-4">
              <input type="radio" id="public" value="public" v-model="visibility" class="form-radio text-blue-500">
              <label for="public" class="ml-2 block text-gray-700 dark:text-gray-300">
                <span class="font-semibold">Public</span>
                <span class="block text-sm text-gray-600 dark:text-gray-400">Any user can see and commit to this model</span>
              </label>
            </div>
            <div class="border-t border-gray-300 dark:border-gray-700"></div>
            <div :class="{'bg-gray-200': visibility === 'private'}" class="flex items-center p-4">
              <input type="radio" id="private" value="private" v-model="visibility" class="form-radio text-blue-500">
              <label for="private" class="ml-2 block text-gray-700 dark:text-gray-300">
                <span class="font-semibold">Private</span>
                <span class="block text-sm text-gray-600 dark:text-gray-400">Only members of your project can see and commit to this model</span>
              </label>
            </div>
          </div>
        </div>
        <div class="mt-6">
          <button type="submit" class="w-full bg-blue-500 text-white py-2 rounded-lg shadow-md hover:bg-blue-700 focus:outline-none">
            Create Model
          </button>
        </div>
      </form>
      <div v-if="successMessage" class="mt-4 p-4 text-green-700 bg-green-100 border border-green-200 rounded-lg">
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      modelName: '',
      visibility: 'public',  // default value
      successMessage: ''  // Success message state
    };
  },
  methods: {
    async createRepository() {
      try {
        const response = await axios.post('http://localhost:8000/github/create-repo', {
          name: this.modelName,
          private: this.visibility === 'private'
        });
        console.log('Repository created:', response.data);
        this.successMessage = 'Model created successfully!';
        setTimeout(() => {
          this.$router.push({ 
            name: 'Vcardtab', 
            query: { 
              repo: `yms218/${this.modelName}` 
            } 
          });
        }, 1500);  // Delay to show the success message
      } catch (error) {
        console.error('Error creating repository:', error);
      }
    }
  }
}
</script>

<style>
.form-radio:checked {
  border-color: #2563eb;
}
</style>
