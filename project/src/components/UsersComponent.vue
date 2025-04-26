<template>
  <div class="users-component">
    <h2>Current Admins</h2>
    <div class="user-list">
      <div class="user-item" v-for="(user, index) in users" :key="index">
        <i class="fas fa-user-circle user-icon"></i> <!-- Account icon -->
        <span class="user-name">{{ user.name }}</span>
        <span class="user-email">{{ user.email }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Voorbeeld van een lijst van admins (dit kan later dynamisch worden geladen)
const users = ref([
  { name: 'Senne Reekmans', email: 'Senne.reekmans@student.pxl.be' },
  { name: 'Abdulrahman Akil', email: 'Abdulrahman.akil@student.pxl.be' },
  { name: 'Milan Frees', email: 'Milan.frees@student.pxl.be' },
  { name: 'Xander Thijs', email: 'Xander.thijs2@student.pxl.be' }
]);
</script>

<style scoped>
.users-component {
  background-color: #2c2c2c;
  width: 100%;
  height: 100%;
  padding: 20px;
  border-radius: 10px;
  color: #ffffff;
  display: flex;
  flex-direction: column;
}

.users-component h2 {
  margin-bottom: 20px;
  color: #fff;
  font-size: 1.5em;
}

.user-list {
  display: flex;
  flex-direction: column;
}

.user-item {
  background-color: #333333;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-item:hover {
  background-color: #680eee;
}

.user-name, .user-email {
  font-size: 1em;
}

.user-name {
  font-weight: bold;
  flex: 1; /* Takes all available space, aligning email to the right */
}

.user-email {
  color: #aaa;
  text-align: right; /* Ensures the email is aligned to the right */
}

.user-icon {
  font-size: 1.5em;
  margin-right: 10px; /* Space between icon and text */
  color: #ffffff;
}
</style>
