<script setup lang="ts">
import { computed } from 'vue';
import { useRouter, RouterView } from 'vue-router';
import { authState, logout } from './store/auth';

const isAuthenticated = computed(() => authState.isAuthenticated);
const user = computed(() => authState.user);
const router = useRouter();

function handleLogout(): void {
  logout();
  router.replace({ name: 'login' });
}
</script>

<template>
  <v-app>
    <v-app-bar density="comfortable" color="primary" dark>
      <v-app-bar-title>App</v-app-bar-title>
      <template #append>
        <div v-if="isAuthenticated" class="d-flex align-center" style="gap: 8px">
          <v-avatar size="28" v-if="user?.avatarUrl">
            <img :src="user?.avatarUrl" alt="Avatar" />
          </v-avatar>
          <span class="mr-2">{{ user?.name }}</span>
          <v-btn variant="text" @click="handleLogout">Logout</v-btn>
        </div>
      </template>
    </v-app-bar>
    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<style scoped></style>
