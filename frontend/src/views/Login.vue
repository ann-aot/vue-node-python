<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { signInWithGoogle } from '../store/auth';

const router = useRouter();
const route = useRoute();
const isLoading = ref(false);
const errorMessage = ref<string | null>(null);

const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID as string;
const isClientConfigured = computed(() => !!clientId);

async function handleGoogleLogin(): Promise<void> {
  errorMessage.value = null;
  if (!clientId) {
    errorMessage.value = 'Google Client ID is not configured (VITE_GOOGLE_CLIENT_ID).';
    return;
  }
  isLoading.value = true;
  try {
    await signInWithGoogle({ clientId, prompt: 'select_account' });
    const redirect = (route.query.redirect as string) || '/dashboard';
    router.replace(redirect);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Login failed';
    errorMessage.value = message;
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="12" md="10" lg="9" xl="8">
        <v-card class="pa-6 pa-md-8" elevation="3" style="overflow: visible">
          <v-card-title class="text-h5">Login</v-card-title>
          <v-card-text style="overflow: visible; word-break: break-word">
            <div class="mb-4">Sign in with your Google account.</div>
            <v-alert v-if="errorMessage" type="error" density="compact" class="mb-4">
              {{ errorMessage }}
            </v-alert>
            <v-btn
              color="primary"
              size="large"
              block
              :loading="isLoading"
              :disabled="!isClientConfigured"
              prepend-icon="mdi-google"
              variant="elevated"
              style="overflow: visible; white-space: normal; height: 56px"
              @click="handleGoogleLogin"
            >
              Continue with Google
            </v-btn>
            <div v-if="!isClientConfigured" class="text-caption mt-2">
              Set VITE_GOOGLE_CLIENT_ID in your environment to enable login.
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<style scoped></style>
