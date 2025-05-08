<template>
  <div class="admins-component">
    <h2 class="component-title">Current Admins</h2>

    <!-- Confirm Dialog -->
    <div v-if="showConfirmDialog" class="confirm-dialog">
      <div class="confirm-dialog-content">
        <p>Are you sure you want to delete <strong>{{ adminToDelete }}</strong>?</p>
        <div class="confirm-dialog-buttons">
          <button @click="confirmDeleteAdmin" class="confirm-btn">Yes, delete</button>
          <button @click="cancelDelete" class="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Add admin form -->
    <div v-if="showAdminForm" class="form">
      <div class="form-content">
        <h2>Add Admin</h2>
        <form @submit.prevent="submitForm">
          <div class="input-form">
            <label for="username">Username</label>
            <input type="text" v-model="newAdmin.username" required />
          </div>

          <div class="input-form">
            <label for="email">Email</label>
            <input type="email" v-model="newAdmin.email" required />
          </div>

          <div class="input-form">
            <label for="password">Password</label>
            <input type="password" v-model="newAdmin.password" required />
          </div>

          <div class="input-form">
            <label for="confirmPassword">Confirm Password</label>
            <input type="password" v-model="confirmPassword" required />
          </div>

          <p v-if="passwordMismatch && submitted" style="color: red;">Passwords do not match.</p>

          <button class="formSubmit" type="submit" :class="{ 'active-submit': isFormFilled }">Submit</button>
          <button type="button" @click="cancelForm">Close</button>
        </form>
      </div>
    </div>

    <!-- Add admin button -->
    <div class="input-group">
      <button type="button" @click="requestAddAdmin" class="add-btn">Add Admin</button>
    </div>

    <div class="admin-list">
      <div class="admin-item" v-for="(admin, index) in admins" :key="index">
        <i class="fas fa-admin-circle admin-icon"></i>
        <span class="admin-name">{{ admin.name }}</span>
        <span class="admin-email">{{ admin.email }}</span>
        <button class="delete-btn" @click="requestDeleteAdmin(admin.email)">Delete</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

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
const admins = ref([])
const adminToDelete = ref(null)
const showConfirmDialog = ref(false)
const showAdminForm = ref(false)
const confirmPassword = ref('')
const submitted = ref(false)

const newAdmin = ref({
  username: '',
  email: '',
  password: ''
})

// Computed
const passwordMismatch = computed(() => newAdmin.value.password !== confirmPassword.value)
const isFormFilled = computed(() =>
  newAdmin.value.username && newAdmin.value.email && newAdmin.value.password && confirmPassword.value
)

// Lifecycle
onMounted(async () => {
  await fetchAdmins()
})

// Functions
async function fetchAdmins() {
  try {
    const response = await authFetch('http://localhost:8000/admins')
    const data = await response.json()
    admins.value = data
  } catch (error) {
    console.error('Failed to fetch admins:', error)
  }
}

function requestDeleteAdmin(email) {
  adminToDelete.value = email
  showConfirmDialog.value = true
}

async function confirmDeleteAdmin() {
  if (!adminToDelete.value) return
  try {
    const token = getToken()
    const response = await axios.post(
      'http://localhost:8000/delete-admin',
      { email: adminToDelete.value },
      { headers: { Authorization: `Bearer ${token}` } }
    )

    await fetchAdmins()
    alert(response.data.message)
  } catch (err) {
    console.error('Error deleting admin:', err)
    alert('Failed to delete admin.')
  } finally {
    showConfirmDialog.value = false
    adminToDelete.value = null
  }
}

function cancelDelete() {
  showConfirmDialog.value = false
  adminToDelete.value = null
}

function requestAddAdmin() {
  showAdminForm.value = true
}

function cancelForm() {
  showAdminForm.value = false
  newAdmin.value = { username: '', email: '', password: '' }
  confirmPassword.value = ''
  submitted.value = false
}

async function submitForm() {
  submitted.value = true

  if (passwordMismatch.value) return

  try {
    const token = getToken()
    const response = await axios.post(
      'http://localhost:8000/register-admin',
      newAdmin.value,
      { headers: { Authorization: `Bearer ${token}` } }
    )

    alert(response.data.message)
    cancelForm()
    await fetchAdmins()
  } catch (err) {
    console.error('Error adding admin:', err)
    alert('Failed to add admin.')
  }
}
</script>


<style scoped>
.admins-component {
  background-color: #2c2c2c;
  width: 100%;
  height: 100%;
  padding: 20px;
  border-radius: 10px;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  position: relative;
}

.component-title {
  margin-bottom: 20px;
  color: #fff;
  font-size: 1.5em;
}

.admin-list {
  display: flex;
  flex-direction: column;
}

.admin-item {
  background-color: #333333;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.admin-name, .admin-email {
  font-size: 1em;
}

.admin-name {
  font-weight: bold;
  flex: 1; /* Takes all available space, aligning email to the right */
}

.admin-email {
  color: #aaa;
  text-align: right; /* Ensures the email is aligned to the right */
}

.admin-icon {
  font-size: 1.5em;
  margin-right: 10px; /* Space between icon and text */
  color: #ffffff;
}

.input-group {
  position: absolute;
  top: 1rem;
  right: 1rem;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.add-btn {
  background-color: #680eee;
  border: none;
  color: white;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-btn:hover {
  background-color: #45087e;
}

.delete-btn {
  background-color: #e53935;
  border: none;
  color: white;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.delete-btn:hover {
  background-color: #c62828;
}

.confirm-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.confirm-dialog-content {
  background: #2c2c2c;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  color: white;
  max-width: 300px;
}

.confirm-dialog-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}

.confirm-btn {
  background-color: #d9534f;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 5px;
}

.confirm-btn:hover {
  background-color: #c62828;
}

.cancel-btn {
  background-color: #5bc0de;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 5px;
}

.cancel-btn:hover {
  background-color: #4ea2bc;
}

.input-form {
  margin-bottom: 15px;
}

input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.form {
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

.form-content {
  background-color: #515151;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
}

.form button {
  color: #ffffff;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  margin-left: 10px;
  border-radius: 5px;
}

.form button:hover {
  background-color: #680eee;
}

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

</style>
