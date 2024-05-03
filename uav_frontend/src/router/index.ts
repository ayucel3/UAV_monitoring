import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue' // Updated import reference
import DronesList from '@/views/DronesList.vue'
import TasksList from '@/views/TasksList.vue'
import TaskDetails from '@/components/TaskDetails.vue'

const routes = [
  { path: '/', name: 'Home', component: HomePage }, // Updated component reference
  { path: '/drones', name: 'Drones', component: DronesList },
  { path: '/tasks', name: 'Tasks', component: TasksList },
  {path: '/tasks/:id',name: 'task-details', component: TaskDetails},
  {path: '/drones/:id', name: 'drone-details', component: () => import('@/components/DroneDetails.vue')
  }
  
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router;
