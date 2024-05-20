<template>
  <div class="h-screen p-5 flex flex-col justify-start items-center dark:text-white text-gray-700">
    <div class="tabs relative w-full">
      <button class="tab-button" :class="{ active: currentTab === 'readme' }" @click="currentTab = 'readme'">Readme</button>
      <button class="tab-button" :class="{ active: currentTab === 'repository' }" @click="currentTab = 'repository'">Repository</button>
      <div v-if="currentTab === 'readme'" class="absolute top-0 right-0 flex">
        <button v-if="!editing" class="edit-button" @click="editReadme">Edit</button>
        <button v-if="editing" class="edit-button" @click="saveReadme">Save</button>
        <button v-if="editing" class="edit-button" @click="cancelEdit">Cancel</button>
      </div>
    </div>
    <div class="tab-content">
      <div v-if="currentTab === 'readme'" class="tab-pane readme-content">
        <div v-if="!editing">
          <iframe
            v-if="iframeUrl"
            frameborder="0"
            style="width:100%; height:calc(100vh - 150px);" 
            :src="iframeUrl"
            allow="clipboard-write"
          ></iframe>
        </div>
        <div v-if="editing" class="readme-edit">
          <textarea v-model="readmeContent" class="textarea"></textarea>
        </div>
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
                <span v-if="!copied">Clone</span>
                <span v-else class="text-green-600">&#10003; Copied</span>
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
      iframeUrl: '',
      copied: false,
      editing: false,
      readmeContent: '',
      readmeSha: ''
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
      this.copied = true;
      setTimeout(() => {
        this.copied = false;
      }, 2000); // 2 seconds later, reset the copied state
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
    },
    async fetchReadmeContent() {
      try {
        const response = await axios.get(`http://localhost:8000/repos/${this.owner}/${this.repoName}/file`, {
          params: {
            path: 'README.md'
          }
        });
        this.readmeContent = atob(response.data.content);
        this.readmeSha = response.data.sha;
      } catch (error) {
        console.error('Failed to fetch README content:', error);
      }
    },
    editReadme() {
      this.editing = true;
      this.fetchReadmeContent();
    },
    cancelEdit() {
      this.editing = false;
    },
    async saveReadme() {
      try {
        const response = await axios.put(`http://localhost:8000/github/update-readme?owner=${this.owner}&repo=${this.repoName}`, {
          content: this.readmeContent,
          sha: this.readmeSha
        });
        this.editing = false;
        this.fetchReadmeLink(); // Refresh the iframe content
      } catch (error) {
        console.error('Failed to update README:', error);
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
  position: relative;
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
.edit-button {
  padding: 5px 10px;
  margin-left: 10px;
  font-size: 14px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
}
.edit-button:hover {
  background-color: #e0e0e0;
}
.tab-content {
  width: 100%;
  height: calc(100vh - 150px); /* Adjusted height to account for tabs */
}
.tab-pane {
  width: 100%;
  height: 100%;
}
.readme-content {
  position: relative;
}
.readme-edit {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.textarea {
  flex: 1;
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  resize: none;
  font-size: 16px;
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
  display: inline-block;
  padding: 5px 10px;
  color: #555;
  text-decoration: none;
  font-weight: bold;
  background-color: #f6f8fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}
.clone-button:hover {
  background-color: #e1e4e8;
}
.repository-container {
  background-color: transparent;
  border: none;
}
</style>
