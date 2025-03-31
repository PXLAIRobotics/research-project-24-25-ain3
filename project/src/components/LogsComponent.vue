<template>
  <div class="logs-panel">
    <h2>System Logs</h2>

    <div v-if="loading" class="loading-state">
      <p>Loading logs...</p>
    </div>

    <div v-if="error" class="error-state">
      <p>{{ error }}</p>
    </div>

    <div v-if="logs.length > 0" class="logs-table-container">
      <table class="logs-table">
        <thead>
          <tr>
            <th>Log ID</th>
            <th>Timestamp</th>
            <th>Log Level</th>
            <th>Message</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.id">
            <td>{{ log.id }}</td>
            <td>{{ new Date(log.timestamp).toLocaleString() }}</td>
            <td>{{ log.message }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="logs.length === 0 && !loading" class="no-logs-state">
      <p>No logs available.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const logs = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchLogs = async () => {
  try {
    const response = await axios.get(''); // Replace with your logs API URL
    logs.value = response.data;
  } catch (error) {
    error.value = 'Failed to load logs.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchLogs();
});
</script>

<style scoped>
.logs-panel {
  background-color: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
  color: white;
  width: 100%;
  height: 100%;  /* Ensures it takes up full height */
  display: flex;
  flex-direction: column;
}

.logs-panel h2 {
  margin-bottom: 20px;
  font-size: 1.5em;
}

.loading-state,
.error-state,
.no-logs-state {
  text-align: center;
  margin-top: 20px;
  font-size: 1.2em;
}

.logs-table-container {
  flex-grow: 1;        /* Ensures the table takes available space */
  overflow-y: auto;    /* Allows vertical scrolling for long content */
  margin-top: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.logs-table {
  width: 100%;
  border-collapse: collapse;
}

.logs-table th, .logs-table td {
  padding: 12px;
  border: 1px solid #444;
  text-align: left;
}

.logs-table th {
  background-color: #333;
}

.logs-table tbody tr:nth-child(even) {
  background-color: #2c2c2c;
}

.logs-table tbody tr:hover {
  background-color: #444;
}

.logs-table td {
  color: #ccc;
}

.logs-table td a {
  color: #680eee;
  text-decoration: none;
}

.logs-table td a:hover {
  text-decoration: underline;
}
</style>
