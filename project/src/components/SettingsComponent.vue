<template>
  <div class="settings-panel">
    <h2>Settings</h2>
    <form @submit.prevent="handleSubmit">

      <!-- Idle Timeout Setting -->
      <div class="input-group">
        <label for="idle-timeout">Idle Timeout (in seconds)</label>
        <input type="range" id="idle-timeout" v-model="idleTimeout" min="1" max="300" />
        <span>{{ idleTimeout }} seconds</span>
      </div>

      <!-- Filters Enable/Disable (Slider Checkbox) -->
      <div class="input-group">
        <label for="filters" class="switch">
          Enable Filters
          <input type="checkbox" id="filters" v-model="filtersEnabled" />
          <span class="slider"></span>
        </label>
      </div>

      <!-- Dark Mode/Light Mode (Slider Checkbox) -->
      <div class="input-group">
        <label for="dark-mode" class="switch">
          Enable Dark Mode
          <input type="checkbox" id="dark-mode" v-model="darkMode" />
          <span class="slider"></span>
        </label>
      </div>

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

      <!-- Save Settings Button -->
      <button type="submit" class="submit-btn" :class="{'success': isSavedSuccessfully}">
        <span v-if="isSavedSuccessfully" class="checkmark">✔</span>
        Save Settings
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const idleTimeout = ref(60); // Default to 60 seconds
const filtersEnabled = ref(true); // Default to enabled
const darkMode = ref(true); // Default to dark mode
const isSavedSuccessfully = ref(false);
const showClearLogsConfirmation = ref(false);
const clearLogsSuccess = ref(false);

// Function to prompt for clearing logs
function promptClearLogs() {
  showClearLogsConfirmation.value = true;
}

// Function to cancel clearing logs
function cancelClearLogs() {
  showClearLogsConfirmation.value = false;
}

// Function to handle "Clear Logs" button click
function clearLogs() {
  // Simulate clearing logs (this could be clearing from local storage or an API)
  clearLogsSuccess.value = true;

  // Reset success state after 3 seconds
  setTimeout(() => {
    clearLogsSuccess.value = false;
  }, 3000);

  // Close confirmation box after success
  showClearLogsConfirmation.value = false;
}

// Function to handle the submit action for saving settings
function handleSubmit() {
  // Simulate saving the settings (e.g., API call or localStorage)
  isSavedSuccessfully.value = true;

  // Reset the success state after 3 seconds
  setTimeout(() => {
    isSavedSuccessfully.value = false;
  }, 3000);
}
</script>

<style scoped>
.settings-panel {
  background-color: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
  color: white;
  width: 100%;
}

.settings-panel h2 {
  margin-bottom: 20px;
  font-size: 1.5em;
}

.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.input-group input[type="range"] {
  width: 100%;
  margin-bottom: 5px;
}

.input-group input[type="checkbox"] {
  display: none;
}

.input-group input[type="checkbox"]:checked + .slider {
  background-color: #680eee;
}

.input-group input[type="checkbox"]:checked + .slider:before {
  transform: translateX(26px);
}

.input-group .slider {
  position: relative;
  width: 50px;
  height: 25px;
  background-color: #ccc;
  border-radius: 50px;
  cursor: pointer;
  transition: 0.4s;
  margin-left: 10px;
}

.input-group .slider:before {
  content: "";
  position: absolute;
  height: 17px;
  width: 17px;
  border-radius: 50px;
  background-color: white;
  transition: 0.4s;
  left: 4px;
  top: 4px;
}

.input-group label {
  display: flex;
  align-items: center;
  gap: 10px;
}

.input-group span {
  font-size: 0.9em;
  color: #ccc;
}

button.submit-btn {
  background-color: #190eee;
  color: white;
  padding: 12px 20px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  width: 100%;
  transition: background-color 0.3s ease;
  position: relative;
}

button.submit-btn:hover {
  background-color: #0f08a5;
}

button.submit-btn.success {
  background-color: #28a745; /* Green color for success */
  color: white;
}

button.submit-btn.success .checkmark {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
}

span.checkmark {
  margin-right: 10px;
}

button.clear-logs-btn {
  background-color: #c23c3c;
  color: white;
  padding: 12px 20px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  width: 100%;
  transition: background-color 0.3s ease;
}

button.clear-logs-btn:hover {
  background-color: #9a2929;
}

.confirmation {
  background-color: #333;
  padding: 20px;
  border-radius: 5px;
  color: white;
  margin-top: 10px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
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
  padding: 8px 16px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.confirm-btn:hover {
  background-color: #0f08a5;
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
  margin-top: 10px;
  text-align: center;
  font-size: 1.1em;
}
</style>
