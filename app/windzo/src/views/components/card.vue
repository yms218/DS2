<template>
  <div class="card-page lg:h-screen h-auto p-3">
    <nav class="flex" aria-label="Breadcrumb">
      <ol class="inline-flex items-center space-x-1 md:space-x-3">
        <li class="inline-flex items-center">
          <a href="#" class="inline-flex items-center text-sm font-medium text-gray-700 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white">
            <svg class="mr-2 w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a 1 1 0 001-1v-2a1 1 0 011-1h2a 1 1 0 011 1v2a 1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path>
            </svg>
            Dashboard
          </a>
        </li>
        <li>
          <div class="flex items-center">
            <svg class="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a 1 1 0 010 1.414l-4 4a 1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
            </svg>
            <a href="#" class="ml-1 text-sm font-medium text-gray-700 hover:text-gray-900 md:ml-2 dark:text-gray-400 dark:hover:text-white">Components</a>
          </div>
        </li>
        <li>
          <div class="flex items-center">
            <svg class="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a 1 1 0 010 1.414l-4 4a 1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
            </svg>
            <a href="#" class="ml-1 text-sm font-medium text-gray-700 hover:text-gray-900 md:ml-2 dark:text-gray-400 dark:hover:text-white">Card</a>
          </div>
        </li>
      </ol>
    </nav>
    <div class="mt-5 w-full flex justify-between items-center">
      <div>
        <h1 class="text-2xl text-gray-900 font-medium dark:text-gray-200">
          Models
        </h1>
        <p class="mt-1 text-sm font-normal text-gray-400">
          This page shows a list of GitHub repositories for models. Use the 'Create Model' button to add a new model.
        </p>
      </div>
      <button
        @click="createModel"
        class="bg-blue-500 text-white px-4 py-2 rounded-lg shadow-md hover:bg-blue-700 focus:outline-none"
      >
        Create Model
      </button>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-5">
      <div
        v-for="repo in repositories"
        :key="repo.full_name"
        class="card w-full p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 relative"
        @click="openBlankPage(repo.full_name)"
      >
        <div class="repo-privacy absolute top-2 left-2 px-2 py-1 bg-white border border-gray-300 text-gray-500 text-xs rounded">
          {{ repo.private ? 'Private' : 'Public' }}
        </div>
        <div class="repo-card mt-8" :data-repo="repo.full_name"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { reloadRepoCards } from '../../repo.js';

export default {
  name: 'RepoCardComponent',
  data() {
    return {
      repositories: []
    };
  },
  async mounted() {
    console.log('Component mounted');
    await this.fetchRepositories();
  },
  methods: {
    async fetchRepositories() {
      try {
        const response = await fetch('http://localhost:8000/models');
        const data = await response.json();
        console.log('Fetched Repositories:', data);  // 디버깅을 위해 콘솔에 출력
        this.repositories = data;
        this.initializeRepoCards();
      } catch (error) {
        console.error('Error fetching repositories:', error);
      }
    },
    initializeRepoCards() {
      reloadRepoCards();
    },
    openBlankPage(repo) {
      this.$router.push({ name: 'Vcardtab', query: { repo } });
    },
    createModel() {
      this.$router.push({ name: 'CreateRepoPage' });
    }
  }
}
</script>

<style>
.card {
  width: 300px;
  height: 200px;
  position: relative;
}
.repo-card {
  height: calc(100% - 2rem); /* Privacy 라벨과 겹치지 않도록 조정 */
  border: none !important;
  box-shadow: none !important;
}
.repo-privacy {
  font-size: 12px;
  font-weight: bold;
  color: #6b7280; /* 회색 텍스트 색상 적용 */
}
</style>
