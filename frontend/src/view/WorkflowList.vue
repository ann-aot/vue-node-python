<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { WorkflowInstance } from '../types/workflow';
import {
  listWorkflows,
  startWorkflow as apiStartWorkflow,
  completeUserTask,
} from '../services/workflows';

const loading = ref(false);
const error = ref<string | null>(null);
const instances = ref<WorkflowInstance[]>([]);

async function fetchInstances() {
  loading.value = true;
  error.value = null;
  try {
    instances.value = await listWorkflows();
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : String(e);
  } finally {
    loading.value = false;
  }
}

async function startWorkflow() {
  loading.value = true;
  error.value = null;
  try {
    await apiStartWorkflow('Simple Approval');
    await fetchInstances();
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : String(e);
  } finally {
    loading.value = false;
  }
}

async function approve(instanceId: string, taskId: string) {
  await completeTask(instanceId, taskId, { approved: true });
}

async function reject(instanceId: string, taskId: string) {
  await completeTask(instanceId, taskId, { approved: false });
}

async function completeTask(instanceId: string, taskId: string, data: Record<string, unknown>) {
  loading.value = true;
  error.value = null;
  try {
    await completeUserTask(instanceId, taskId, data);
    await fetchInstances();
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : String(e);
  } finally {
    loading.value = false;
  }
}

onMounted(fetchInstances);
</script>

<template>
  <div>
    <h2>Workflows</h2>
    <button @click="startWorkflow" :disabled="loading">Start Simple Approval</button>
    <div v-if="loading">Loading...</div>
    <div v-if="error" style="color: red">{{ error }}</div>
    <ul>
      <li v-for="wf in instances" :key="wf.id">
        <strong>{{ wf.name }}</strong>
        <span> — {{ wf.status }}</span>
        <div v-if="wf.ready_user_tasks.length">
          <div v-for="t in wf.ready_user_tasks" :key="t.id" style="margin-top: 8px">
            Task: {{ t.name }} ({{ t.spec_name }})
            <button @click="approve(wf.id, t.id)" :disabled="loading">Approve</button>
            <button @click="reject(wf.id, t.id)" :disabled="loading">Reject</button>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
button {
  margin: 0 6px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
}
</style>
