<template>
    <div class="h-screen p-5 flex justify-center dark:text-white text-gray-700">

      <div class="wrapper-button w-full box-border mt-4">
        <button
          type="button"
          class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
          @click="openUrl"  
        >
          Create Model
        </button>
      </div>
    </div>
  </template>
  
<script>
export default {
  methods: {
    openUrl() {
      window.open('http://127.0.0.1:8888/', '_blank');
    }
  }
}
</script>