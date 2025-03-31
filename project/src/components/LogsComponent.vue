<template>
  <div class="log-container">
    <h2>Logs</h2>
    <button @click="fetchLogs">Load logs</button>

    <div class="table-wrapper">
      <div v-if="logs.length">
        <div v-for="(logFile, fileIndex) in logs" :key="fileIndex">
          <h3 class="log-header">Log File #{{ fileIndex + 1 }}</h3>
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
      <p v-else class="no-logs">No logs available.</p>
    </div>
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
        console.log("Fetched data:", data);
        this.logs = data.logs;
      } catch (error) {
        console.error("Error fetching logs:", error);
      }
    },
    rowClass(log) {
      return log.role === "error" ? "error-row" : "";
    },
    codeClass(code) {
      if (code >= 400) return "code-red";
      if (code >= 300) return "code-orange";
      if (code >= 200) return "code-green";
      return "code-gray";
    }
  }
};
</script>

<style scoped>
.log-container {
  padding: 1rem;
  background: var(--color-background-soft);
  color: var(--color-text);
}

h2 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: var(--color-heading);
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
  border: 1px solid var(--color-border);
  background-color: var(--color-background);
  padding: 10px;
  border-radius: 8px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
}

.table-wrapper::-webkit-scrollbar {
  width: 8px;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: var(--color-border-hover);
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: var(--color-background-soft);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

th {
  background: var(--color-background-mute);
  position: sticky;
  top: 0;
  z-index: 1;
  color: var(--color-heading);
}

tr:nth-child(even) {
  background: var(--color-background-soft);
}

tr:hover {
  background: var(--color-background-mute);
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
  font-size: 1.2rem;
  font-weight: bold;
  background-color: var(--color-background-mute);
  padding: 8px;
  margin-top: 10px;
  border-left: 5px solid #4dff88;
  color: #4dff88;
}

.no-logs {
  color: var(--color-text);
  text-align: center;
  padding: 1rem;
}
</style>
