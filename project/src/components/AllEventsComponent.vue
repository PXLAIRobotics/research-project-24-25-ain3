<template>
  <div class="events-panel">
    <h2>All Events</h2>

    <div v-if="loading" class="loading-state">
      <p>Loading events...</p>
    </div>

    <div v-if="error" class="error-state">
      <p>{{ error }}</p>
    </div>

    <div v-if="events.length > 0" class="events-table-container">
      <table class="events-table">
        <thead>
          <tr>
            <th>Event ID</th>
            <th>Event Name</th>
            <th>Event Date</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="event in events" :key="event.id">
            <td>{{ event.id }}</td>
            <td>{{ event.event_name }}</td>
            <td>{{ new Date(event.event_date).toLocaleDateString() }}</td>
            <td>{{ event.event_description }}</td>
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
import { ref, onMounted } from 'vue';
import axios from 'axios';

const events = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchEvents = async () => {
  try {
    const response = await axios.get('http://localhost:8000/allEvents');
    events.value = response.data.events; 
    console.log('Fetched events:', events.value);
  } catch (err) {
    error.value = 'Failed to load events.';
  } finally {
    loading.value = false;
  }
};
onMounted(() => {
  fetchEvents();
});
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
</style>
