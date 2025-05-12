<template>
  <div class="addevents-panel">
    <h2>Add Events</h2>

    <div v-if="loading" class="loading-state">
      <p>Loading...</p>
    </div>

   

    <label>
      Campus:
      <input v-model="campusName" placeholder="Corda" />
    </label>

    <div v-for="(category, index) in eventCategories" :key="index" class="event-category">
      <h3>{{ category.name }}</h3>

      <div v-for="(event, idx) in category.events" :key="idx" class="event-item">
        <input v-model="event.name" placeholder="Name" />
        <input v-model="event.date" type="date" />
        <input v-model="event.description" placeholder="Description" />
      </div>

      <button @click="addEvent(index)">+ Add {{ category.name }} event</button>
    </div>

    <div class="error-state" :style="{ minHeight: '24px' }">
  <p v-if="error">{{ error }}</p>
  </div>
    <button @click="submitEvents" class="submit-btn">Submit Events</button>
  </div>
  
</template>

<script setup>
import { ref } from 'vue'

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
const loading = ref(false)
const error = ref('')
const campusName = ref('Corda')

const eventCategories = ref([
  { name: 'Academic', events: [{ name: '', date: '', description: '' }] },
  { name: 'Cultural', events: [{ name: '', date: '', description: '' }] },
  { name: 'Workshops', events: [{ name: '', date: '', description: '' }] },
  { name: 'Social', events: [{ name: '', date: '', description: '' }] },
])

const addEvent = (index) => {
  eventCategories.value[index].events.push({ name: '', date: '', description: '' })
}

const submitEvents = async () => {
  loading.value = true
  error.value = ''

  const formattedEvents = {}
  for (const category of eventCategories.value) {
    formattedEvents[category.name] = category.events.filter(e => e.name && e.date && e.description)
  }

  const payload = {
    campus_name: campusName.value,
    events: formattedEvents
  }

  try {
    const response = await authFetch('http://localhost:8000/events', {
      method: 'POST',
      body: JSON.stringify(payload)
    })
    const result = await response.json()
    console.log('Success:', result)
  } catch (err) {
    console.error('Error:', err)
    error.value = 'Failed to submit events.'
  } finally {
    loading.value = false
  }
}
</script>


<style scoped>
.addevents-panel {
  background-color: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
  color: white;
  width: 100%;
  height: 100vh; /* Volledige hoogte van het scherm */
  overflow-y: auto; /* Scrollen als de inhoud te groot is */
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.event-category {
  margin-bottom: 10px;
}

.event-item {
  display: flex;
  gap: 10px;
  margin-bottom: 5px;
}

input {
  padding: 5px;
  border-radius: 5px;

}

.submit-btn {
  padding: 10px;
  background-color: #4caf50;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 0px;
}

.submit-btn:hover {
  background-color: #45a049;
}

.error-state {
  color: red;
  min-height: 24px;
  transition: opacity 0.3s ease;
}

.error-state p {
  margin: 0;
}

</style>
