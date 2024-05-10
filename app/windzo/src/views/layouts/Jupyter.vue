<template>
  <div class="h-screen p-5 flex flex-col justify-center items-center dark:text-white text-gray-700">
    <div class="wrapper-button w-full box-border mb-4">
      <button
        type="button"
        class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
        @click="openUrl"
      >
        Create Model
      </button>
    </div>
    <!-- HTML 컨텐츠 렌더링 -->
    <div class="readme-container markdown-body" v-html="readmeHtml"></div>
  </div>
</template>

<script>
import axios from 'axios';
import 'github-markdown-css'

export default {
  data() {
    return {
      readmeHtml: '', // HTML 컨텐츠 저장
    };
  },
  methods: {
    openUrl() {
      window.open('http://127.0.0.1:8888/', '_blank');
    },
    fetchReadme() {
      axios.get('http://localhost:5000/github/yms218/DS2/readme')
        .then(response => {
          this.readmeHtml = response.data;  // 서버로부터 받은 HTML을 저장
        })
        .catch(error => {
          console.error('Error fetching README:', error);
          this.readmeHtml = '<p>Error loading README content.</p>';
        });
    }
  },
  mounted() {
    this.fetchReadme();  // 컴포넌트 마운트 시 README 로드
  }
}
</script>

<style>
.readme-container {
  padding: 20px;
  /* background: #f1adad;
  border: 1px solid #ddd; */
  overflow-y: auto; 
  max-height: 70vh; 
}
</style>
