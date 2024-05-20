<template>
  <div id="app">
    <RepoTree owner="yms218" repo="DS2"/>
  </div>
</template>

<script>
import RepoTree from "./tree.vue";

export default {
  name: 'App',
  components: {
    RepoTree
  }
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
}
ul {
  list-style-type: none;
  padding-left: 20px;
}
li {
  cursor: pointer;
  margin: 5px 0;
}
</style>