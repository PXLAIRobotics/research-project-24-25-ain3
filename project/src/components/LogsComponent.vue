<template>
  <div class="log-container">
    <h2>System Logs</h2>

    <!-- Confirm Dialog -->
    <div v-if="showConfirmDialog" class="confirm-dialog">
      <div class="confirm-dialog-content">
        <p>Are you sure you want to delete <strong>ALL logs</strong>?</p>
        <div class="confirm-dialog-buttons">
          <button @click="confirmDeleteLogs" class="confirm-btn">Yes, delete</button>
          <button @click="cancelDelete" class="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Clear Logs Button -->
    <div class="input-group">
      <button type="button" @click="requestDeleteLogs" class="delete-btn">Clear Logs</button>
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
import { ref, onMounted } from 'vue'

// Helpers
function getToken() {
  return localStorage.getItem('token')
}

async function authFetch(url, options = {}) {
  const token = getToken()
  const headers = {
    ...options.headers,
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
  const response = await fetch(url, { ...options, headers })
  if (response.status === 401) {
    alert('Session expired or unauthorized.')
    throw new Error('Unauthorized')
  }
  return response
}

// State
const logs = ref([])
const loading = ref(true)
const error = ref(null)
const showConfirmDialog = ref(false)
const clearLogsSuccess = ref(false)
const collapsedLogs = ref([])
const eventToDelete = ref(null)

// Fetch logs from backend
const fetchLogs = async () => {
  loading.value = true
  try {
    const response = await authFetch('http://ec2-16-171-142-19.eu-north-1.compute.amazonaws.com:8000/logs')
    const data = await response.json()
    logs.value = data.logs
    collapsedLogs.value = logs.value.map((_, index) => index)
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load logs.'
  } finally {
    loading.value = false
  }
}

// Request confirmation
const requestDeleteLogs = () => {
  showConfirmDialog.value = true
}

// Confirm and delete logs
const confirmDeleteLogs = async () => {
  try {
    const response = await authFetch('http://ec2-16-171-142-19.eu-north-1.compute.amazonaws.com:8000/clear-logs', {
      method: 'POST',
    })
    const result = await response.json()
    logs.value = []
    clearLogsSuccess.value = true

    setTimeout(() => {
      clearLogsSuccess.value = false
    }, 3000)
  } catch (err) {
    console.error('Error deleting logs:', err)
    alert('Failed to delete logs.')
  } finally {
    showConfirmDialog.value = false
    eventToDelete.value = null
  }
}

const cancelDelete = () => {
  showConfirmDialog.value = false
  eventToDelete.value = null
}

const rowClass = (log) => {
  return log.role === 'error' ? 'error-row' : ''
}

const codeClass = (code) => {
  if (code >= 400) return 'code-red'
  if (code >= 300) return 'code-orange'
  if (code >= 200) return 'code-green'
  return 'code-gray'
}

const toggleCollapse = (fileIndex) => {
  if (collapsedLogs.value.includes(fileIndex)) {
    collapsedLogs.value = collapsedLogs.value.filter(index => index !== fileIndex)
  } else {
    collapsedLogs.value.push(fileIndex)
  }
}

onMounted(() => {
  fetchLogs()
})
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
  top: 45px;
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

.delete-btn {
  background-color: #e53935;
  border: none;
  color: white;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.delete-btn:hover {
  background-color: #c62828;
}

.confirm-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.confirm-dialog-content {
  background: #2c2c2c;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  color: white;
  max-width: 300px;
}

.confirm-dialog-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}

.confirm-btn {
  background-color: #d9534f;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 5px;
}

.confirm-btn:hover {
  background-color: #c62828;
}

.cancel-btn {
  background-color: #5bc0de;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 5px;
}

.cancel-btn:hover {
  background-color: #4ea2bc;
}

</style>