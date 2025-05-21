<template>
  <div class="events-panel">
    <h2>All Events</h2>

    <div v-if="loading" class="loading-state">
      <p>Loading events...</p>
    </div>

    <div v-if="error" class="error-state">
      <p>{{ error }}</p>
    </div>

    <!-- Confirm Dialog -->
    <div v-if="showConfirmDialog" class="confirm-dialog">
      <div class="confirm-dialog-content">
        <p>Are you sure you want to delete <strong>{{ eventToDelete }}</strong>?</p>
        <div class="confirm-dialog-buttons">
          <button @click="confirmDeleteEvent" class="confirm-btn">Yes, delete</button>
          <button @click="cancelDelete" class="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>

    <div v-if="events.length > 0" class="events-table-container">
      <table class="events-table">
        <thead>
          <tr>
            <th>Event ID</th>
            <th>Event Name</th>
            <th>Event Date</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="event in events" :key="event.id">
            <td>{{ event.id }}</td>
            <td>{{ event.event_name }}</td>
            <td>{{ new Date(event.event_date).toLocaleDateString() }}</td>
            <td>{{ event.event_description }}</td>
            <td>
              <button class="delete-btn" @click="requestDeleteEvent(event.event_name)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="events.length === 0 && !loading" class="no-events-state">
      <p>No events available.</p>
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
const events = ref([])
const loading = ref(true)
const error = ref(null)
const eventToDelete = ref(null)
const showConfirmDialog = ref(false)

// Fetch events with token
const fetchEvents = async () => {
  loading.value = true
  try {
    const response = await authFetch('https://wealthy-current-cat.ngrok-free.app/allEvents')
    const data = await response.json()
    events.value = data.events
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load events.'
  } finally {
    loading.value = false
  }
}

// Delete logic
const requestDeleteEvent = (eventName) => {
  eventToDelete.value = eventName
  showConfirmDialog.value = true
}

const confirmDeleteEvent = async () => {
  if (!eventToDelete.value) return
  try {
    const response = await authFetch('https://wealthy-current-cat.ngrok-free.app/delete-event', {
      method: 'POST',
      body: JSON.stringify({ name: eventToDelete.value })
    })
    const result = await response.json()
    if (result.success || result.message) {
      events.value = events.value.filter(event => event.event_name !== eventToDelete.value)
    }
  } catch (err) {
    console.error('Error deleting event:', err)
    alert('Failed to delete event.')
  } finally {
    showConfirmDialog.value = false
    eventToDelete.value = null
  }
}

const cancelDelete = () => {
  showConfirmDialog.value = false
  eventToDelete.value = null
}

// Lifecycle
onMounted(() => {
  fetchEvents()
})
</script>


<style scoped>
.events-panel {
  background-color: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
  color: white;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.events-panel h2 {
  margin-bottom: 20px;
  font-size: 1.5em;
}

.loading-state,
.error-state,
.no-events-state {
  text-align: center;
  margin-top: 20px;
  font-size: 1.2em;
}

.events-table-container {
  flex-grow: 1;
  overflow-y: auto;
  margin-top: 20px;
  max-height: 400px;
}

.events-table {
  width: 100%;
  border-collapse: collapse;
}

.events-table th, .events-table td {
  padding: 12px;
  border: 1px solid #444;
  text-align: left;
}

.events-table th {
  background-color: #333;
}

.events-table tbody tr:nth-child(even) {
  background-color: #2c2c2c;
}

.events-table tbody tr:hover {
  background-color: #444;
}

.events-table td {
  color: #ccc;
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

.cancel-btn {
  background-color: #5bc0de;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 5px;
}

</style>
