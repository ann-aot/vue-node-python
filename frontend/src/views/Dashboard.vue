<script setup lang="ts">
import { computed, ref } from 'vue';
import { authState } from '../store/auth';

const user = computed(() => authState.user);
const editingDob = ref(false);
const dobLocal = ref<string | null>(authState.user?.dob ?? null);

function startEditDob(): void {
  dobLocal.value = authState.user?.dob ?? null;
  editingDob.value = true;
}

async function saveDob(): Promise<void> {
  const apiBase = import.meta.env.VITE_API_BASE_URL as string | undefined;
  if (!apiBase || !authState.user) {
    editingDob.value = false;
    return;
  }
  authState.user.dob = dobLocal.value ?? undefined;
  fetch(`${apiBase}/api/v1/users/google`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      google_sub: authState.user.id,
      email: authState.user.email,
      name: authState.user.name,
      avatar_url: authState.user.avatarUrl,
      dob: dobLocal.value,
    }),
  })
    .then((r) => r.ok ? r.json() : null)
    .then((saved) => {
      if (saved && authState.user) {
        authState.user.dob = saved.dob ?? authState.user.dob;
        authState.user.name = saved.name ?? authState.user.name;
        authState.user.email = saved.email ?? authState.user.email;
        authState.user.avatarUrl = saved.avatar_url ?? authState.user.avatarUrl;
      }
    })
    .catch(() => undefined);
  editingDob.value = false;
}
</script>

<template>
  <v-container class="py-8">
    <h2 class="text-h5 mb-4">Dashboard</h2>
    <v-row align="start" justify="center">
      <v-col cols="12" sm="10" md="8" lg="7" xl="6">
        <v-card elevation="3" class="pa-4 pa-md-6">
          <v-card-text>
            <div v-if="user">
              <div class="d-flex align-center mb-4" style="gap: 12px">
                <v-avatar size="56" v-if="user.avatarUrl">
                  <img :src="user.avatarUrl" alt="Avatar" />
                </v-avatar>
                <div>
                  <div class="text-subtitle-1">{{ user.name }}</div>
                  <div class="text-body-2">{{ user.email }}</div>
                </div>
              </div>
              <v-divider class="my-4" />
              <div class="text-subtitle-2 mb-2">Profile details</div>
              <v-list density="comfortable">
                <v-list-item title="Name" :subtitle="user.name" />
                <v-list-item title="Email" :subtitle="user.email" />
                <v-list-item>
                  <template #title>DOB</template>
                  <template #subtitle>
                    <div v-if="!editingDob">{{ user.dob || 'Not set' }}</div>
                    <div v-else class="d-flex align-center" style="gap: 8px">
                      <v-text-field
                        v-model="dobLocal"
                        type="date"
                        density="compact"
                        hide-details
                        style="max-width: 220px"
                      />
                      <v-btn size="small" color="primary" @click="saveDob">Save</v-btn>
                      <v-btn size="small" variant="text" @click="editingDob = false">Cancel</v-btn>
                    </div>
                  </template>
                  <template #append>
                    <v-btn
                      size="small"
                      variant="text"
                      @click="startEditDob()"
                      v-if="!editingDob"
                    >
                      Edit
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>
            </div>
            <div v-else>Loading...</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped></style>
