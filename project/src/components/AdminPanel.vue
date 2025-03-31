<template>
  <div class="admin-panel">
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
          <div class="input-group">
            <label for="email">Email</label>
            <input type="email" v-model="email" required />
          </div>
          <div class="input-group">
            <label for="password">Password</label>
            <input type="password" v-model="password" required />
          </div>
          <button class="formSubmit" type="submit" :class="{ 'active-submit': isFormFilled }">Submit</button>
          <button @click="closeModal">Close</button>
        </form>
      </div>
    </div>

    <header>
      <img src="../assets/corda-logo.png" @click="handleClick" alt="Logo" class="header-logo" />
      <h1>VIBE</h1>
      <div>
        <button @click="toggleSidebar">Toggle Sidebar</button>
        <button class="logout" @click="logout">Logout</button>
      </div>
    </header>

    <div class="main-content">
      <div class="sidebar" :class="{ hidden: !isSidebarVisible }">
        <ul>
          <button @click="activePanel = 'dashboard'">Dashboard</button>
          <button @click="activePanel = 'users'">Users</button>
          <button @click="activePanel = 'settings'">Settings</button>
          <button @click="activePanel = 'logs'">Logs</button>
          <button @click="activePanel = 'reports'">Reports</button>
        </ul>
      </div>

      <main>
        <div v-if="activePanel === 'dashboard'" class="dashboard-view">
          <UsersComponent />
          <SettingsComponent />
          <LogsComponent />
          <ReportsComponent />
        </div>
        <UsersComponent v-else-if="activePanel === 'users'" class="expanded" />
        <SettingsComponent v-else-if="activePanel === 'settings'" class="expanded" />
        <LogsComponent v-else-if="activePanel === 'logs'" class="expanded" />
        <ReportsComponent v-else-if="activePanel === 'reports'" class="expanded" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import UsersComponent from '../components/UsersComponent.vue';
import SettingsComponent from '../components/SettingsComponent.vue';
import LogsComponent from '../components/LogsComponent.vue';
import ReportsComponent from '../components/ReportsComponent.vue';

const email = ref('')
const password = ref('')
const showModal = ref(true)

const isFormFilled = computed(() => email.value !== '' && password.value !== '')
const isSidebarVisible = ref(true)
const activePanel = ref('dashboard');
const router = useRouter()

const correctEmail = 'admin@gmail.com' // Replace with your email
const correctPassword = 'admin' // Replace with your password

onMounted(() => {
  // Show the modal on page load
  showModal.value = true
})

function handleLogin() {
  // Check if the email and password are correct
  if (email.value === correctEmail && password.value === correctPassword) {
    showModal.value = false // Hide the modal after successful login
    router.push('/admin') // Redirect to the admin panel page
  } else {
    alert('Invalid credentials')
  }
}

function closeModal() {
  router.push({ name: 'interfaceComponent' });
}

function toggleSidebar() {
  isSidebarVisible.value = !isSidebarVisible.value
}

function logout() {
  localStorage.removeItem('userToken')
  router.push('/')
}

const handleClick = () => {
  router.push({ name: 'interfaceComponent' });
};
</script>

<style>
.active-submit {
  color: white;
}

.formSubmit {
  margin-bottom: 10px;
}
form {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #515151;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
}

.input-group {
  margin-bottom: 15px;
}

input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

#app {
  width: 100%;
  height: 100%;
}

.admin-panel {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #1e1e1e;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #333333;
  padding: 10px 20px;
  width: 100%;
  box-sizing: border-box;
}

header h1 {
  margin: 0;
  color: #ffffff;
}

.header-logo {
  width: 85px;
  height: 50px;
  margin-right: 10px;
}

button {
  color: #ffffff;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  margin-left: 10px;
  border-radius: 5px;
}

button:hover {
  background-color: #680eee;
}

.logout:hover {
  background-color: red;
}

.main-content {
  display: flex;
  flex-grow: 1;
}

.sidebar {
  width: 200px;
  background-color: #2c2c2c;
  color: #ffffff;
  padding-top: 20px;
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.sidebar.hidden {
  transform: translateX(-150%);
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sidebar button {
  width: 90%;
  text-align: center;
  padding: 12px;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.sidebar button:hover {
  background-color: #680eee;
}

main {
  flex-grow: 1;
  padding: 20px;
  background-color: #1e1e1e;
  color: #ffffff;
  overflow-y: auto; /* Enable vertical scrolling */
  height: calc(100vh - 60px); /* Adjust this height if needed */
}


.dashboard-view {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-gap: 20px;
  grid-template-rows: auto;
  max-width: 100%;
  overflow: hidden;
}

.dashboard-view > * {
  max-width: 100%;
  overflow: hidden;
}

.expanded {
  grid-column: span 2;
  width: 100%;
  height: 100%;
  max-height: 100%;
  overflow: hidden;
}

@media (max-width: 768px) {
  .sidebar {
    width: 60%;
  }
}

@media (max-width: 480px) {
  .sidebar {
    width: 100%;
  }

  .dashboard-view {
    grid-template-columns: 1fr;
  }
}
</style>
