<template>
  <div>
    <!-- Header should be outside the centered div -->
    <Header />

    <!-- Main content -->
    <div class="app-content">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from './components/Header.vue';
</script>

<style>
.app-content {
  margin: 20px;
  padding: 0 15px;
  box-sizing: border-box;
}
</style>
