<template>
  <div class="outer-container">
    <div class="tree-container">
      <div class="header-container">
        <div class="commit-header">
          <img :src="commitAuthorAvatar" alt="avatar" class="avatar">
          <span class="author">{{ commitAuthorName }}</span>
          <span class="message">{{ latestCommitMessage }}</span>
          <span class="timestamp">{{ latestCommitTime }}</span>
        </div>
      </div>
      <div class="breadcrumbs-container">
        <div class="breadcrumbs">
          <span @click="navigateTo(-1)">.</span>
          <span v-for="(segment, index) in pathSegments" :key="index" @click="navigateTo(index)">
            / {{ segment }}
          </span>
        </div>
      </div>
      <ul class="file-list">
        <li v-for="item in filteredTree" :key="item.path" @dblclick="handleClick(item)">
          <span v-if="item.type === 'tree'">📁</span>
          <span v-else>📄</span>
          {{ item.path.split('/').pop() }}
          <span class="commit-message">{{ item.commit.message }}</span>
          <span class="commit-time">{{ timeSince(item.commit.timestamp) }} ago</span>
        </li>
      </ul>
      <div v-if="selectedFileContent" class="file-content">
        <h3>{{ selectedFilePath }}</h3>
        <pre>{{ selectedFileContent }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    owner: {
      type: String,
      required: true
    },
    repo: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      tree: [],
      currentPath: '',
      selectedFilePath: '',
      selectedFileContent: '',
      latestCommit: null,
      commitAuthorName: '',
      commitAuthorAvatar: '',
      latestCommitMessage: '',
      latestCommitTime: ''
    };
  },
  computed: {
    pathSegments() {
      return this.currentPath.split('/').filter(segment => segment);
    },
    filteredTree() {
      const currentPathLength = this.currentPath.length;
      return this.tree.filter(item => {
        const itemPath = item.path;
        if (this.currentPath === '') {
          return !itemPath.includes('/');
        }
        return itemPath.startsWith(this.currentPath + '/') && itemPath.slice(currentPathLength + 1).indexOf('/') === -1;
      });
    }
  },
  methods: {
    async fetchRepoData() {
      const commitsResponse = await axios.get(`https://api.github.com/repos/${this.owner}/${this.repo}/commits`);
      const treeResponse = await axios.get(`https://api.github.com/repos/${this.owner}/${this.repo}/git/trees/main?recursive=1`);

      this.latestCommit = commitsResponse.data[0];
      this.commitAuthorName = this.latestCommit.commit.author.name;
      this.commitAuthorAvatar = this.latestCommit.author.avatar_url;
      this.latestCommitMessage = this.latestCommit.commit.message;
      this.latestCommitTime = this.timeSince(this.latestCommit.commit.author.date) + ' ago';
      
      this.tree = treeResponse.data.tree.map(item => {
        return {
          ...item,
          commit: {
            message: this.latestCommit.commit.message,
            timestamp: this.latestCommit.commit.author.date
          }
        };
      });
    },
    async handleClick(item) {
      if (item.type === 'tree') {
        this.currentPath = item.path;
      } else if (item.type === 'blob') {
        this.selectedFilePath = item.path;
        const response = await axios.get(`https://raw.githubusercontent.com/${this.owner}/${this.repo}/main/${item.path}`);
        this.selectedFileContent = response.data;
      }
    },
    navigateTo(index) {
      if (index === -1) {
        this.currentPath = '';
      } else {
        this.currentPath = this.pathSegments.slice(0, index + 1).join('/');
      }
    },
    timeSince(date) {
      const seconds = Math.floor((new Date() - new Date(date)) / 1000);
      let interval = seconds / 31536000;
      if (interval > 1) return Math.floor(interval) + " years";
      interval = seconds / 2592000;
      if (interval > 1) return Math.floor(interval) + " months";
      interval = seconds / 86400;
      if (interval > 1) return Math.floor(interval) + " days";
      interval = seconds / 3600;
      if (interval > 1) return Math.floor(interval) + " hours";
      interval = seconds / 60;
      if (interval > 1) return Math.floor(interval) + " minutes";
      return Math.floor(seconds) + " seconds";
    }
  },
  mounted() {
    this.fetchRepoData();
  }
};
</script>

<style>
.outer-container {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
}

.tree-container {
  width: 100%;
  max-width: 800px;
  background-color: #ffffff;
  padding: 0;
  box-sizing: border-box;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
}

.header-container {
  background-color: #f5f5f5;
  padding: 10px 20px;
  border-radius: 8px 8px 0 0;
}

.breadcrumbs-container {
  padding: 10px 20px;
  background-color: transparent;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 14px; /* 글씨 크기 1px 작게 조정 */
  background-color: transparent; /* 배경색 없애기 */
}

.breadcrumbs span {
  cursor: pointer;
  color: #0366d6;
}

.breadcrumbs span:hover {
  text-decoration: underline;
}

.commit-header {
  display: flex;
  align-items: center;
  font-size: 14px; /* 글씨 크기 1px 작게 조정 */
}

.commit-header .avatar {
  width: 36px; /* 기존 40px에서 36px로 축소 */
  height: 36px;
  border-radius: 50%;
  margin-right: 10px;
}

.commit-header .author {
  font-weight: bold;
  margin-right: 10px;
}

.commit-header .message {
  margin-right: 10px;
}

.commit-header .timestamp {
  color: #888;
}

.file-list {
  list-style: none;
  padding: 0 20px;
  margin: 0;
  background-color: transparent; /* 배경색 없애기 */
}

.file-list li {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
  font-size: 14px; /* 글씨 크기 1px 작게 조정 */
}

.file-list .commit-message {
  margin-left: 20px;
  color: #666;
}

.file-list .commit-time {
  color: #888;
}

.file-content {
  width: 100%;
  border-top: 1px solid #ddd;
  margin-top: 10px;
  padding-top: 10px;
  font-size: 14px; /* 글씨 크기 1px 작게 조정 */
}

.file-content h3 {
  margin-bottom: 10px;
}

.file-content pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background-color: #f6f8fa;
  padding: 10px;
  border-radius: 5px;
  max-width: 100%;
  width: 100%;
  box-sizing: border-box;
}
</style>
