<template>
  <div class="settings-panel">
    <h2>Settings</h2>
    <form @submit.prevent="handleSubmit">

      <!-- Idle Timeout Setting -->
      <div class="input-group">
        <label for="idle-timeout">Idle Timeout (in seconds)</label>
        <input type="range" id="idle-timeout" v-model="idleTimeout" min="15" max="300" step="5" />
        <span>{{ idleTimeout }} seconds</span>
      </div>

      <!-- Filters Enable/Disable (Slider Checkbox) -->
      <div class="input-group">
        <label for="filters" class="switch">
          Enable Filters (In Development)
          <input type="checkbox" id="filters" v-model="filtersEnabled" />
          <span class="slider"></span>
        </label>
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
import axios from 'axios';

// Saved values
const savedIdleTimeout = ref(120);
const savedFiltersEnabled = ref(true);

// Editable fields (linked to UI)
const idleTimeout = ref(savedIdleTimeout.value);
const filtersEnabled = ref(savedFiltersEnabled.value);

// UI state
const isSavedSuccessfully = ref(false);

// Save settings function
function handleSubmit() {
  // Save current UI values into saved values
  savedIdleTimeout.value = idleTimeout.value;
  savedFiltersEnabled.value = filtersEnabled.value;

  // Save to localStorage
  localStorage.setItem('idleTimeout', savedIdleTimeout.value);
  localStorage.setItem('filtersEnabled', savedFiltersEnabled.value);

  // Show success
  isSavedSuccessfully.value = true;

  // Reset after 3 seconds
  setTimeout(() => {
    isSavedSuccessfully.value = false;
  }, 3000);
}

// Load saved settings from localStorage if they exist
if (localStorage.getItem('idleTimeout')) {
  const storedTimeout = parseInt(localStorage.getItem('idleTimeout'), 10);
  savedIdleTimeout.value = storedTimeout;
  idleTimeout.value = storedTimeout;
}

if (localStorage.getItem('filtersEnabled')) {
  const storedFiltersEnabled = localStorage.getItem('filtersEnabled') === 'true';
  savedFiltersEnabled.value = storedFiltersEnabled;
  filtersEnabled.value = storedFiltersEnabled;
}
</script>

<style scoped>
.settings-panel {
  background-color: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
  color: white;
  width: 100%;
  max-width: 100%; /* Ensure it does not get restricted */
  flex-grow: 1; /* Allow it to grow if inside a flex container */
  overflow: visible; /* Ensure the content can overflow */
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
  background-color: #680eee;
  color: white;
  padding: 12px 20px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  width: 100%;
  transition: background-color 0.3s ease;
  position: relative;
  margin-left: 0px;
}

button.submit-btn:hover {
  background-color: #45087e;
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

</style>
