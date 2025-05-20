<template>
  <div class="admins-component">
    <h2 class="component-title">Current Admins</h2>

    <!-- Confirm Dialog -->
    <div v-if="showConfirmDialog" class="confirm-dialog">
      <div class="confirm-dialog-content">
        <p>Are you sure you want to delete <strong>{{ adminToDelete.username }}</strong>?</p>
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

          <p class="error-form" v-if="passwordMismatch && submitted" >Passwords do not match.</p>
          <p class="error-form" v-if="duplicateEmail && submitted" >Email already in use.</p>

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
        <button v-if="admin.email === currentUserEmail" class="current-btn">Current</button>
        <button v-if="admin.email !== currentUserEmail" class="delete-btn" @click="requestDeleteAdmin(admin.email)">Delete</button>
      </div>
    </div>

    <!-- Success message -->
    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

function getToken() {
  return localStorage.getItem('token')
}

function getCurrentUserEmail() {
  return localStorage.getItem('adminEmail')
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

const admins = ref([])
const adminToDelete = ref(null)
const showConfirmDialog = ref(false)
const showAdminForm = ref(false)
const confirmPassword = ref('')
const submitted = ref(false)
const successMessage = ref('')
const currentUserEmail = ref(getCurrentUserEmail())

const newAdmin = ref({
  username: '',
  email: '',
  password: ''
})

const passwordMismatch = computed(() => newAdmin.value.password !== confirmPassword.value)
const isFormFilled = computed(() =>
  newAdmin.value.username && newAdmin.value.email && newAdmin.value.password && confirmPassword.value
)

onMounted(async () => {
  await fetchAdmins()
})

async function fetchAdmins() {
  try {
    const response = await authFetch('http://ec2-16-171-142-19.eu-north-1.compute.amazonaws.com:8000/admins')
    const data = await response.json()
    admins.value = data
  } catch (error) {
    console.error('Failed to fetch admins:', error)
  }
}

function requestDeleteAdmin(email) {
  if (email === currentUserEmail.value) {
    alert("You cannot delete your own account.")
    return
  }
  const admin = admins.value.find(a => a.email === email)
  if (admin) {
    adminToDelete.value = { username: admin.name, email: admin.email }
    showConfirmDialog.value = true
  }
}


async function confirmDeleteAdmin() {
  if (!adminToDelete.value) return
  try {
    const token = getToken()
    const response = await axios.post(
      'http://ec2-16-171-142-19.eu-north-1.compute.amazonaws.com:8000/delete-admin',
      {
        username: adminToDelete.value.username,
        email: adminToDelete.value.email
      },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    await fetchAdmins()
    showSuccess(response.data.message)
  } catch (err) {
    console.error('Error deleting admin:', err)
    successMessage.value = 'Failed to delete admin.'
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
  duplicateEmail.value = false
}


const duplicateEmail = ref(false)

async function submitForm() {
  submitted.value = true
  duplicateEmail.value = false

  if (passwordMismatch.value) return

  const emailExists = admins.value.some(admin => admin.email === newAdmin.value.email)
  if (emailExists) {
    duplicateEmail.value = true
    return
  }

  try {
    const token = getToken()
    const response = await axios.post(
      'http://ec2-16-171-142-19.eu-north-1.compute.amazonaws.com:8000/register-admin',
      newAdmin.value,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    cancelForm()
    await fetchAdmins()
    showSuccess(response.data.message)
  } catch (err) {
    console.error('Error adding admin:', err)
    successMessage.value = 'Failed to add admin.'
  }
}

function showSuccess(message) {
  successMessage.value = message
  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
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
  margin: 5px 0px;
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
  flex: 1;
}

.admin-email {
  color: #aaa;
  text-align: right;
}

.admin-icon {
  font-size: 1.5em;
  margin-right: 10px;
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

.delete-btn, .current-btn {
  width: 100px;
  background-color: #e53935;
  border: none;
  color: white;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.current-btn {
  background-color: #680eee;
}

.current-btn:hover {
  cursor: default;
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
  background-color: #680eee;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  margin-left: 0px;
  border-radius: 5px;
}

.form button:hover {
  background-color: #45087e;
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

.success-message {
  margin-top: 1rem;
  color: #4caf50;
  font-weight: bold;
  padding: 10px 15px;
  border-radius: 5px;
  text-align: center;
}

.error-form {
  color: #d9534f;
  font-weight: bold;
  margin: 5px;
}

</style>
