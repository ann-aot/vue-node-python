<script setup lang="ts">
import { computed, ref } from 'vue';
import { authState } from '../store/auth';

const user = computed(() => authState.user);
const editingDob = ref(false);
const dobLocal = ref<string | null>(authState.user?.dob ?? null);
const dobDialog = ref(false);

function startEditDob(): void {
  dobLocal.value = authState.user?.dob ?? null;
  editingDob.value = true;
  dobDialog.value = true;
}

async function saveDob(): Promise<void> {
  const apiBaseEnv = import.meta.env.VITE_API_BASE_URL as string | undefined;
  const apiBase = apiBaseEnv && apiBaseEnv.length > 0 ? apiBaseEnv : 'http://localhost:8300';
  if (!authState.user) {
    editingDob.value = false;
    return;
  }
  authState.user.dob = dobLocal.value ?? undefined;
  fetch(`${apiBase}/api/v1/users/${authState.user.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      dob: dobLocal.value,
    }),
  })
    .then((r) => (r.ok ? r.json() : null))
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
  dobDialog.value = false;
}

function cancelDob(): void {
  editingDob.value = false;
  dobDialog.value = false;
}
</script>

<template>
  <v-container class="py-8" fluid>
    <h2 class="text-h5 mb-4">Dashboard</h2>
    <v-row align="start" justify="center">
      <v-col cols="12" sm="12" md="11" lg="10" xl="9">
        <v-card elevation="3" class="pa-4 pa-md-6" style="overflow: visible">
          <v-card-text style="overflow: visible; word-break: break-word">
            <div v-if="user">
              <div class="d-flex align-center mb-4" style="gap: 12px">
                <v-avatar size="56" v-if="user.avatarUrl">
                  <img :src="user.avatarUrl" alt="Avatar" />
                </v-avatar>
                <div>
                  <div class="text-subtitle-1" style="word-break: break-word">{{ user.name }}</div>
                  <div class="text-body-2" style="word-break: break-word">{{ user.email }}</div>
                </div>
              </div>
              <v-divider class="my-4" />
              <div class="text-subtitle-2 mb-2">Profile details</div>
              <v-list density="comfortable" style="overflow: visible">
                <v-list-item>
                  <template #title>Name</template>
                  <template #subtitle>
                    <div style="white-space: normal; word-break: break-word">{{ user.name }}</div>
                  </template>
                </v-list-item>
                <v-list-item>
                  <template #title>Email</template>
                  <template #subtitle>
                    <div style="white-space: normal; word-break: break-word">{{ user.email }}</div>
                  </template>
                </v-list-item>
                <v-list-item>
                  <template #title>DOB</template>
                  <template #subtitle>
                    <div>{{ user.dob || 'Not set' }}</div>
                  </template>
                  <template #append>
                    <v-btn size="small" variant="text" @click="startEditDob()">Edit</v-btn>
                  </template>
                </v-list-item>
              </v-list>
              <v-dialog v-model="dobDialog" max-width="360">
                <v-card>
                  <v-card-title class="text-h6">Select date of birth</v-card-title>
                  <v-card-text>
                    <v-text-field v-model="dobLocal" type="date" label="DOB" hide-details />
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer />
                    <v-btn variant="text" @click="cancelDob">Cancel</v-btn>
                    <v-btn color="primary" @click="saveDob">Save</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </div>
            <div v-else>Loading...</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped></style>
