<template>
  <div class="h-screen p-5 flex flex-col justify-start items-center dark:text-white text-gray-700">
    <div class="tabs">
      <button class="tab-button" :class="{ active: currentTab === 'readme' }" @click="currentTab = 'readme'">Readme</button>
      <button class="tab-button" :class="{ active: currentTab === 'repository' }" @click="currentTab = 'repository'">Repository</button>
    </div>
    <div class="tab-content">
      <div v-if="currentTab === 'readme'" class="tab-pane">
        <iframe
          v-if="iframeUrl"
          frameborder="0"
          style="width:100%; height:100%;"
          :src="iframeUrl"
          allow="clipboard-write"
        ></iframe>
      </div>
      <div v-if="currentTab === 'repository'" class="tab-pane">
        <div class="repository-container">
          <div class="repository-header">
            <div class="breadcrumbs">
              <span v-for="(segment, index) in pathSegments" :key="index" @click="navigateTo(index)">
                / {{ segment }}
              </span>
            </div>
            <div class="clone-container">
              <input type="text" class="clone-url" :value="cloneUrl" readonly />
              <button class="clone-button" @click="copyCloneUrl">
                <svg class="clone-icon" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true">
                  <path fill-rule="evenodd" d="M0 1.75A.75.75 0 01.75 1h13.5a.75.75 0 010 1.5H13v12a.75.75 0 01-.75.75H1.75A.75.75 0 011 14.5V2h-.25A.75.75 0 010 1.75zM2 3.5v10.25h10.5V3.5H2zm10.75-2h1.5a.75.75 0 010 1.5h-1.5a.75.75 0 010-1.5zM1 3.5h10.5V14H1V3.5zM3.5 0a.75.75 0 01.75.75v1.5A.75.75 0 013.5 3h-2a.75.75 0 010-1.5h1.25V.75A.75.75 0 013.5 0zm9.5 0a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0v-1.5A.75.75 0 0113 0zm1.5 12.75A.75.75 0 0114 12h1.5a.75.75 0 010 1.5H14a.75.75 0 01-.75-.75zm-.75-9.75a.75.75 0 011.5 0v1.5a.75.75 0 01-1.5 0V3zM.75 9A.75.75 0 010 8.25v-1.5a.75.75 0 011.5 0v1.5A.75.75 0 01.75 9zM0 4.75A.75.75 0 01.75 4h1.5a.75.75 0 010 1.5h-1.5A.75.75 0 010 4.75z"></path>
                </svg>
                Clone
              </button>
            </div>
          </div>
          <keep-alive>
            <RepoTree ref="repoTree" :owner="owner" :repo="repoName" />
          </keep-alive>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RepoTree from "../components/tree.vue";
import axios from 'axios';

export default {
  name: 'App',
  components: {
    RepoTree
  },
  props: {
    repo: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      currentTab: 'readme',
      scriptLoaded: false,
      iframeUrl: ''
    };
  },
  computed: {
    owner() {
      return this.repo ? this.repo.split('/')[0] : '';
    },
    repoName() {
      return this.repo ? this.repo.split('/')[1] : '';
    },
    cloneUrl() {
      return `git@github.com:${this.repo}.git`;
    },
    pathSegments() {
      return this.$refs.repoTree ? this.$refs.repoTree.currentPath.split('/').filter(segment => segment) : [];
    }
  },
  methods: {
    copyCloneUrl() {
      const el = document.createElement('textarea');
      el.value = this.cloneUrl;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      alert('Clone URL copied to clipboard!');
    },
    loadRepoScript() {
      const script = document.createElement('script');
      script.src = '//iframely.net/embed.js';
      document.head.appendChild(script);
      script.onload = () => {
        this.scriptLoaded = true;
      };
    },
    navigateTo(index) {
      if (this.$refs.repoTree) {
        this.$refs.repoTree.navigateTo(index);
      }
    },
    async fetchReadmeLink() {
      try {
        const response = await axios.get('http://localhost:8000/github/readme-link', {
          params: {
            owner: this.owner,
            repo: this.repoName
          }
        });
        this.iframeUrl = response.data.iframe_url;
      } catch (error) {
        console.error('Failed to fetch README link:', error);
      }
    }
  },
  watch: {
    currentTab(newTab) {
      if (newTab === 'repository' && !this.scriptLoaded) {
        this.loadRepoScript();
      } else if (newTab === 'readme') {
        this.fetchReadmeLink();
      }
    }
  },
  created() {
    // repo 값이 유효한지 확인
    if (!this.repo) {
      console.error('repo 값이 전달되지 않았습니다.');
    } else {
      console.log('Received repo:', this.repo);
      this.fetchReadmeLink();
    }
  }
}
</script>

<style>
.tabs {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  margin-bottom: 10px;
  border-bottom: 2px solid #e0e0e0;
}
.tab-button {
  padding: 10px 15px;
  margin: 0;
  cursor: pointer;
  background: none;
  border: none;
  font-size: 16px;
  color: #888;
  transition: color 0.3s ease, border-bottom 0.3s ease;
}
.tab-button.active {
  color: black;
  border-bottom: 2px solid black;
}
.tab-button:not(.active):hover {
  color: #555;
}
.tab-content {
  width: 100%;
  height: calc(100vh - 150px); /* Adjusted height to account for tabs */
}
.tab-pane {
  width: 100%;
  height: 100%;
}

.repository-container {
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 10px;
  width: 100%;
  height: 100%;
  margin: 0 auto;
  background-color: #ffffff;
}
.repository-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.breadcrumbs {
  display: flex;
  align-items: center;
  color: #0366d6;
}
.breadcrumbs span {
  margin-right: 5px;
  cursor: pointer;
}
.breadcrumbs span:hover {
  text-decoration: underline;
}
.clone-container {
  display: flex;
  align-items: center;
}
.clone-url {
  padding: 5px;
  margin-right: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f6f8fa;
  color: #333;
  font-size: 0.875rem;
  width: 300px;
}
.clone-button {
  display: flex;
  align-items: center;
  color: #0366d6;
  text-decoration: none;
  font-weight: bold;
  background: none;
  border: none;
  cursor: pointer;
}
.clone-icon {
  margin-right: 5px;
}
</style>
