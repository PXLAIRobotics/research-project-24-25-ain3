<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-4">API Logs</h2>
    <button @click="fetchLogs" class="mb-4 px-4 py-2 bg-blue-500 text-white rounded">
      Laad logs
    </button>
    <table class="min-w-full border border-gray-300 shadow-lg" v-if="logs.length">
      <thead class="bg-gray-200">
        <tr>
          <th class="border p-2">Role</th>
          <th class="border p-2">Message</th>
          <th class="border p-2">Response Code</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(log, index) in logs" :key="index" :class="rowClass(log)">
          <td class="border p-2 font-bold">{{ log.role }}</td>
          <td class="border p-2">{{ log.content }}</td>
          <!-- Show response_code if it exists, else show N/A -->
          <td v-if="log.response_code" class="border p-2 font-bold" :class="codeClass(log.response_code)">
            {{ log.response_code }}
          </td>
          <td v-else class="border p-2">N/A</td> <!-- For logs without a response_code -->
        </tr>
      </tbody>
    </table>
    <p v-else class="text-gray-500">Geen logs beschikbaar.</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      logs: []
    };
  },
  methods: {
    async fetchLogs() {
      try {
        const response = await fetch("http://localhost:8000/logs");
        const data = await response.json();
        console.log("Fetched data:", data);  // Verify structure
        this.logs = data.logs || [];
      } catch (error) {
        console.error("Error fetching logs:", error);
      }
    },
    rowClass(log) {
      // Highlight the row if the log role is "error"
      return log.role === "error" ? "bg-red-100 text-red-800" : "bg-white";
    },
    codeClass(code) {
      // Color the response code based on its value
      if (code >= 400) return "text-red-600";  // Error code
      if (code >= 300) return "text-orange-500";  // Redirect code
      if (code >= 200) return "text-green-600";  // Success code
      return "text-gray-700";  // Default code
    }
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
}
</style>
