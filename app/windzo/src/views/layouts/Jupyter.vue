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
    <!-- GitHub 리포지토리 카드를 동적으로 생성 -->
    <div v-for="repo in repositories" :key="repo" class="repo-card" :data-repo="repo"></div>
  </div>
</template>

<script>
export default {
  name: 'RepoCardComponent',
  data() {
    return {
      // 리포지토리 목록을 저장
      repositories: [
                      "yms218/Code-Up-Algorithm",
                      "yms218/Deep-Learning",
                      "yms218/DS-SNU-12th-Project",
                      "yms218/DS2",
                      "yms218/Embeded-Lecture",
                      "yms218/linux",
                      "yms218/MLOps",
                      "yms218/POSCO_9th_A_Algorithm"
                    ]
    };
  },
  mounted() {
    this.loadRepoScript();
  },
  methods: {
    openUrl() {
      window.open('http://127.0.0.1:8888/hub', '_blank');
    },
    loadRepoScript() {
      const script = document.createElement('script');
      script.src = 'https://tarptaeya.github.io/repo-card/repo-card.js';
      script.onload = () => {
        if (window.tarptaeya && window.tarptaeya.reloadRepoCards) {
          window.tarptaeya.reloadRepoCards();
        }
      };
      document.head.appendChild(script);
    }
  }
}
</script>

<style>
/* 여기에 필요한 스타일을 추가할 수 있습니다 */
</style>
