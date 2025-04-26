<template>
  <div class="log-container">
    <h2>System Logs</h2>

    <div v-if="loading" class="loading-state">
      <p>Loading logs...</p>
    </div>

    <div v-if="error" class="error-state">
      <p>{{ error }}</p>
    </div>

    <div class="table-wrapper">
      <div v-if="logs.length">
        <div v-for="(logFile, fileIndex) in logs" :key="fileIndex">
          <h3 class="log-header" @click="toggleCollapse(fileIndex)">
            Log File #{{ fileIndex + 1 }}
            <span class="collapse-icon">{{ collapsedLogs.includes(fileIndex) ? '+' : '-' }}</span>
          </h3>
          
          <div v-show="!collapsedLogs.includes(fileIndex)">
            <table>
              <thead>
                <tr>
                  <th>Role</th>
                  <th>Message</th>
                  <th>Response Code</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(log, logIndex) in logFile" :key="logIndex" :class="rowClass(log)">
                  <td class="bold-text">{{ log.role }}</td>
                  <td>{{ log.content }}</td>
                  <td v-if="log.response_code" :class="codeClass(log.response_code)">
                    {{ log.response_code }}
                  </td>
                  <td v-else>N/A</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <p v-else-if="!loading" class="no-logs">No logs available.</p>
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
    const response = await axios.get('http://localhost:8000/logs'); // <- Update if needed
    console.log('Fetched data:', response.data);
    logs.value = response.data.logs;

    // Auto-collapse all log files
    collapsedLogs.value = logs.value.map((_, index) => index);
  } catch (err) {
    console.error('Error fetching logs:', err);
    error.value = 'Failed to load logs.';
  } finally {
    loading.value = false;
  }
};

const rowClass = (log) => {
  return log.role === "error" ? "error-row" : "";
};

const codeClass = (code) => {
  if (code >= 400) return "code-red";
  if (code >= 300) return "code-orange";
  if (code >= 200) return "code-green";
  return "code-gray";
};

const collapsedLogs = ref([]);

const toggleCollapse = (fileIndex) => {
  if (collapsedLogs.value.includes(fileIndex)) {
    collapsedLogs.value = collapsedLogs.value.filter(index => index !== fileIndex);
  } else {
    collapsedLogs.value.push(fileIndex);
  }
};


onMounted(() => {
  fetchLogs();
});
</script>

<style scoped>
.log-container {
  padding: 1rem;
  background: var(--color-background-soft, #2c2c2c);
  color: var(--color-text, white);
}

h2 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.loading-state,
.error-state,
.no-logs {
  text-align: center;
  margin-top: 20px;
  font-size: 1.2em;
}

button {
  background-color: #190eee;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  transition: background 0.3s ease-in-out;
}

button:hover {
  background-color: #0f08c2;
}

.table-wrapper {
  max-height: 600px;
  overflow-y: auto;
  border: 1px solid var(--color-border, #444);
  background-color: var(--color-background, #333);
  padding: 10px;
  border-radius: 8px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
}

.table-wrapper::-webkit-scrollbar {
  width: 8px;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: var(--color-border-hover, #666);
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: var(--color-background-soft, #2c2c2c);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--color-border, #444);
}

th {
  background: var(--color-background-mute, #333);
  position: sticky;
  top: 0;
  z-index: 1;
}

tr:nth-child(even) {
  background: var(--color-background-soft, #2c2c2c);
}

tr:hover {
  background: var(--color-background-mute, #444);
}

.error-row {
  background-color: #4a1414;
  color: #ff6666;
}

.code-red {
  color: #ff4d4d;
  font-weight: bold;
}

.code-orange {
  color: #ffb84d;
  font-weight: bold;
}

.code-green {
  color: #4dff88;
  font-weight: bold;
}

.code-gray {
  color: #bbb;
}

.log-header {
  position: sticky;
  top: 0; /* Sticks at the very top */
  z-index: 3; /* Higher z-index to be above thead */
  background-color: var(--color-background-mute, #333);
  padding: 8px;
  margin-top: 10px;
  border-left: 5px solid #4dff88;
  color: #4dff88;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.collapse-icon {
  font-size: 1.2rem;
  padding-left: 10px;
}

table thead th {
  position: sticky;
  top: 40px; /* Push down by header height (adjust if header is taller) */
  background-color: var(--color-background-mute, #333);
  z-index: 2;
}

</style>
