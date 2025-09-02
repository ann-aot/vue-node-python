<script setup lang="ts">
import { computed } from 'vue';
import { authState } from '../store/auth';

const user = computed(() => authState.user);
</script>

<template>
  <v-container class="py-8">
    <h2 class="text-h5 mb-4">Dashboard</h2>
    <v-card>
      <v-card-text>
        <div v-if="user">
          <div class="d-flex align-center mb-4" style="gap: 12px">
            <v-avatar size="48" v-if="user.avatarUrl">
              <img :src="user.avatarUrl" alt="Avatar" />
            </v-avatar>
            <div>
              <div class="text-subtitle-1">{{ user.name }}</div>
              <div class="text-body-2">{{ user.email }}</div>
            </div>
          </div>
          <div>Welcome to your dashboard.</div>
        </div>
        <div v-else>Loading...</div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<style scoped></style>
