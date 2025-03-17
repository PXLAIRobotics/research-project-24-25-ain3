<template>
  <div class="admin-panel">
    <header>
      <img src="../assets/corda-logo.png" alt="Logo" class="header-logo" />
      <h1>VIBE</h1>
      <div>
        <button @click="toggleSidebar">Toggle Sidebar</button>
        <button @click="logout">Logout</button>
      </div>
    </header>

    <div class="main-content">
      <div class="sidebar" :class="{ hidden: !isSidebarVisible }">
        <ul>
          <li><router-link to="/" active-class="active">Dashboard</router-link></li>
          <li><router-link to="/users" active-class="active">Users</router-link></li>
          <li><router-link to="/settings" active-class="active">Settings</router-link></li>
          <li><router-link to="/reports" active-class="active">Logs</router-link></li>
        </ul>
      </div>

      <main>
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const isSidebarVisible = ref(true)
const router = useRouter()

function toggleSidebar() {
  isSidebarVisible.value = !isSidebarVisible.value
}

function logout() {
  localStorage.removeItem('userToken')
  router.push('/login')
}
</script>


<style>
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
  background-color: #190eee;
  color: #ffffff;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  margin-left: 10px;
  border-radius: 5px;
}

button:hover {
  background-color: #190eee;
}

button.logout:hover {
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
}

.sidebar.hidden {
  transform: translateX(-150%);
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar li {
  padding: 15px;
  text-align: center;
}

.sidebar li a {
  color: #ffffff;
  text-decoration: none;
  display: block;
  border-radius: 5px;
}

.sidebar li a:hover,
.sidebar li a.active {
  background-color: #190eee;
  font-weight: bold;
}

main {
  flex-grow: 1;
  padding: 20px;
  background-color: #1e1e1e;
  color: #ffffff;
}
</style>
