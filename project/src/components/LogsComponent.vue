<template>
  <div class="log-container">
    <h2>System Logs</h2>

    <!-- Clear Logs Button -->
    <div class="input-group">
      <button type="button" @click="promptClearLogs" class="clear-logs-btn">Clear Logs</button>
      <div v-if="showClearLogsConfirmation" class="confirmation">
        <p>Are you sure you want to clear the logs?</p>
        <div class="confirmation-buttons">
          <button @click="clearLogs" class="confirm-btn">Yes</button>
          <button @click="cancelClearLogs" class="cancel-btn">No</button>
        </div>
      </div>
      <p v-if="clearLogsSuccess" class="success-message">Logs cleared successfully!</p>
    </div>

    <div class="table-wrapper">
      <div v-if="loading" class="loading-state">
        <p>Loading logs...</p>
      </div>

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
      <p v-else-if="!loading && !error" class="no-logs">No logs available.</p>
      <p v-else-if="error" class="error-state">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const logs = ref([]);
const loading = ref(true);
const error = ref(null);
const showClearLogsConfirmation = ref(false);
const clearLogsSuccess = ref(false);
const collapsedLogs = ref([]);

const fetchLogs = async () => {
  loading.value = true;
  try {
    const response = await axios.get('http://localhost:8000/logs');
    logs.value = response.data.logs;

    // Auto-collapse all log files
    collapsedLogs.value = logs.value.map((_, index) => index);
  } catch (err) {
    error.value = 'Failed to load logs.';
  } finally {
    loading.value = false;
  }
};

// Prompt for clearing logs
const promptClearLogs = () => {
  showClearLogsConfirmation.value = true;
};

// Cancel clearing logs
const cancelClearLogs = () => {
  showClearLogsConfirmation.value = false;
};

// Handle clear logs functionality
const clearLogs = async () => {
  try {
    // Clear logs from backend (adjust the API call as per your backend setup)
    await axios.post('http://localhost:8000/clear-logs');
    
    // Clear the logs in the frontend
    logs.value = [];
    clearLogsSuccess.value = true;

    // Reset success state after 3 seconds
    setTimeout(() => {
      clearLogsSuccess.value = false;
    }, 3000);

    // Close confirmation modal
    showClearLogsConfirmation.value = false;
  } catch (err) {
    error.value = 'Failed to clear logs.';
  }
};

// Row class based on log role
const rowClass = (log) => {
  return log.role === "error" ? "error-row" : "";
};

// Response code color class
const codeClass = (code) => {
  if (code >= 400) return "code-red";
  if (code >= 300) return "code-orange";
  if (code >= 200) return "code-green";
  return "code-gray";
};

// Toggle collapse for log files
const toggleCollapse = (fileIndex) => {
  if (collapsedLogs.value.includes(fileIndex)) {
    collapsedLogs.value = collapsedLogs.value.filter(index => index !== fileIndex);
  } else {
    collapsedLogs.value.push(fileIndex);
  }
};

// Automatically load logs on mount
onMounted(() => {
  fetchLogs();
});
</script>

<style scoped>
.log-container {
  padding: 1rem;
  background: #2c2c2c;
  color: white;
  position: relative;
  border-radius: 10px;
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

.table-wrapper {
  max-height: 600px;
  overflow-y: auto;
  border: 1px solid #444;
  background-color: #333;
  padding: 10px;
  border-radius: 8px;
  position: relative;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #2c2c2c;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #444;
}

th {
  background-color: #2c2c2c;
  font-weight: bold;
  position: sticky;
  top: 0;
  z-index: 2;
}

tr:nth-child(even) {
  background: #2c2c2c;
}

tr:hover {
  background: #444;
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
  top: 0;
  z-index: 3;
  background-color: #333;
  padding: 8px;
  border-left: 5px solid #4dff88;
  color: #4dff88;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.log-header:hover {
  background-color: #444;
  color: #76ffb4;
}

.collapse-icon {
  font-size: 1.2rem;
  padding-left: 10px;
}

.input-group {
  position: absolute;
  top: 1rem;
  right: 1rem;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

button.clear-logs-btn {
  background-color: #c23c3c;
  color: white;
  padding: 10px 16px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

button.clear-logs-btn:hover {
  background-color: #9a2929;
}

.confirmation {
  background-color: #333;
  padding: 15px;
  border-radius: 5px;
  color: white;
  margin-top: 5px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 250px;
  position: absolute;
  top: 60px; /* Adjust as needed */
  right: 0;
  z-index: 1000; /* Make sure it stays on top */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}


.confirmation-buttons {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

.confirm-btn,
.cancel-btn {
  background-color: #680eee;
  color: white;
  padding: 6px 14px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.confirm-btn:hover {
  background-color: #45087e;
}

.cancel-btn {
  background-color: #c23c3c;
}

.cancel-btn:hover {
  background-color: #9a2929;
}

.success-message {
  color: #28a745;
  font-weight: bold;
  margin-top: 8px;
  text-align: center;
  font-size: 1em;
}
</style>