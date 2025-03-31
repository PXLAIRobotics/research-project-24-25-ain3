<template>
  <div class="reports-panel">
    <h2>User Reports</h2>

    <div v-if="loading" class="loading-state">
      <p>Loading reports...</p>
    </div>

    <div v-if="error" class="error-state">
      <p>{{ error }}</p>
    </div>

    <div v-if="reports.length > 0" class="reports-table-container">
      <table class="reports-table">
        <thead>
          <tr>
            <th>Report ID</th>
            <th>User ID</th>
            <th>Report Date</th>
            <th>Details</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="report in reports" :key="report.id">
            <td>{{ report.id }}</td>
            <td>{{ report.userId }}</td>
            <td>{{ new Date(report.date).toLocaleDateString() }}</td>
            <td>{{ report.details }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="reports.length === 0 && !loading" class="no-reports-state">
      <p>No reports available.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const reports = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchReports = async () => {
  try {
    const response = await axios.get('');
    reports.value = response.data;
  } catch (error) {
    error.value = 'Failed to load reports.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchReports();
});
</script>

<style scoped>
.reports-panel {
  background-color: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
  color: white;
  width: 100%;
  height: 100%;  /* Ensures it takes up full height */
  display: flex;
  flex-direction: column;
}

.reports-panel h2 {
  margin-bottom: 20px;
  font-size: 1.5em;
}

.loading-state,
.error-state,
.no-reports-state {
  text-align: center;
  margin-top: 20px;
  font-size: 1.2em;
}

.reports-table-container {
  flex-grow: 1;        /* Ensures the table takes available space */
  overflow-y: auto;    /* Allows vertical scrolling for long content */
  margin-top: 20px;
}

.reports-table {
  width: 100%;
  border-collapse: collapse;
}

.reports-table th, .reports-table td {
  padding: 12px;
  border: 1px solid #444;
  text-align: left;
}

.reports-table th {
  background-color: #333;
}

.reports-table tbody tr:nth-child(even) {
  background-color: #2c2c2c;
}

.reports-table tbody tr:hover {
  background-color: #444;
}

.reports-table td {
  color: #ccc;
}

.reports-table td a {
  color: #680eee;
  text-decoration: none;
}

.reports-table td a:hover {
  text-decoration: underline;
}

</style>
