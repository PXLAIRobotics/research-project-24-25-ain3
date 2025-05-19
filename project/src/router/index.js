import { createRouter, createWebHistory } from 'vue-router'

// Import your components for routing
import DashboardComponent from '../components/DashboardComponent.vue'
import UsersComponent from '../components/UsersComponent.vue'
import SettingsComponent from '../components/SettingsComponent.vue'
import LogsComponent from '../components/LogsComponent.vue'
import ChatComponent from '../components/ChatComponent.vue'
import HomePageComponent from '../components/homePage.vue'
import InterfaceComponent from '../components/InterfaceComponent.vue'
import AdminComponent from '../components/AdminPanel.vue'
import LoginComponent from '../components/LoginComponent.vue'

// Define routes
const routes = [
  { path: '/dashboard', component: DashboardComponent },
  { path: '/users', component: UsersComponent },
  { path: '/settings', component: SettingsComponent },
  { path: '/logs', component: LogsComponent },
  { path: '/chat', component: ChatComponent },
  { path: '/',  component: HomePageComponent },
  { path: '/interface', name: "interfaceComponent",  component: InterfaceComponent },
  { path: '/admin', name: "adminComponent",  component: AdminComponent },
  { path : '/login', name: "loginComponent",  component: LoginComponent },
]

// Create router instance
const router = createRouter({
  history: createWebHistory('/research-project-24-25-ain3/'),
  routes,
})

export default router
