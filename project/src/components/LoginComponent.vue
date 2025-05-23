<template>
  <div class="login-panel">
    <div class="modal">
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
          <button @click="closeModal" type="button">Close</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { API_BASE_URL } from '@/config.js'

const email = ref('')
const password = ref('')
const router = useRouter()

const isFormFilled = computed(() => email.value !== '' && password.value !== '')

async function handleLogin() {
  try {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value })
    })

    if (!response.ok) throw new Error('Login failed')

    const data = await response.json()

    localStorage.setItem('token', data.access_token)
    localStorage.setItem('adminEmail', email.value)

    router.push('/admin')
  } catch (error) {
    alert('Invalid credentials or session expired')
    console.error(error)
  }
}

function closeModal() {
  router.push('/')
}
</script>

<style scoped>
.login-panel {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #333333;
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

form {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
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

.formSubmit {
  margin-bottom: 10px;
}

.active-submit {
  color: white;
}

button {
  background-color: #680eee;
  border: none;
  color: white;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-left: 0px;
}

button:hover {
  background-color: #45087e;
}

</style>
  