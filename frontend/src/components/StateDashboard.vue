<template>
  <div class="state-dashboard">
    <h2>States Dashboard</h2>

    <!-- Loading -->
    <div v-if="loading">Loading states...</div>

    <!-- Error -->
    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <!-- Table -->
    <table v-else class="state-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>State Name</th>
          <th>Population</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="state in states" :key="state.id">
          <td>{{ state.id }}</td>
          <td>{{ state.name }}</td>
          <td>{{ state.population }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import type { RootState } from '@/store/types';
import { ActionTypes } from '@/store/modules/states/actions';
//

export default defineComponent({
  name: 'StateDashboard',
  setup() {
    const store = useStore<RootState>();

    // Fetch states on mount
    onMounted(() => {
      store.dispatch(`states/${ActionTypes.FETCH_STATES}`);
    });

    // Map state from getters
    const states = computed(() => store.getters['states/allStates']);
    const loading = computed(() => store.getters['states/isLoading']);
    const error = computed(() => store.getters['states/errorMessage']);

    return {
      states,
      loading,
      error,
    };
  },
});
</script>

<style scoped>
.state-dashboard {
  margin: 20px;
}

.state-table {
  width: 100%;
  border-collapse: collapse;
}

.state-table th,
.state-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.state-table th {
  background-color: #f4f4f4;
  text-align: left;
}

.error {
  color: red;
  font-weight: bold;
}
</style>
