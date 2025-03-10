import { createRouter, createWebHistory } from 'vue-router'

// Import your components for routing
import Dashboard from '../components/DashboardComponent.vue'
import Users from '../components/UsersComponent.vue'
import Settings from '../components/SettingsComponent.vue'
import Logs from '../components/LogsComponent.vue'

// Define routes
const routes = [
  { path: '/', component: Dashboard },
  { path: '/users', component: Users },
  { path: '/settings', component: Settings },
  { path: '/logs', component: Logs },
]

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard to protect routes
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('userToken')
  if (to.path !== '/login' && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
