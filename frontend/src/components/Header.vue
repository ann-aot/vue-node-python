<template>
  <header class="header">
    <div class="left-section">
      <!-- Logo -->
      <img src="/logo-banner.png" alt="Logo" class="logo" />
      <!-- Header text -->
      <h1 class="header-text">Vue + Python + TS</h1>
    </div>

    <!-- User dropdown -->
    <div class="right-section" @click="toggleDropdown">
      <span class="user-name">{{ userName }}</span>
      <div v-if="showDropdown" class="dropdown">
        <ul>
          <li @click="signOut">Sign Out</li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const userName = ref('John Doe'); // hardcoded for now
const showDropdown = ref(false);

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

const signOut = () => {
  alert('Signing out...');
  showDropdown.value = false;
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #003366;
  color: white;
  padding: 10px 20px;
  width: 100%; /* full width */
  box-sizing: border-box;
  margin: 0;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 50px;
}

.logo {
  height: 40px;
  margin-right: 12px;
}

.header-text {
  font-size: 20px;
  font-weight: bold;
}

.right-section {
  position: relative;
  cursor: pointer;
}

.user-name {
  font-weight: 500;
}

.dropdown {
  position: absolute;
  right: 0;
  top: 100%;
  background: white;
  color: black;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 120px;
  z-index: 1000;
}

.dropdown ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.dropdown li {
  padding: 8px 12px;
  cursor: pointer;
}

.dropdown li:hover {
  background-color: #f1f1f1;
}
</style>
