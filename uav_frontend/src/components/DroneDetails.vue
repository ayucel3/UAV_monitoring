<template>
    <div class="max-w-4xl mx-auto mt-10 p-5 bg-white shadow-lg rounded-lg">
      <h1 class="text-3xl font-bold mb-6 text-gray-800 text-center">{{ droneName }}</h1>
        <h2 class="text-xl font-semibold text-gray-700 mb-4">Tasks</h2>
      <ul v-if="tasks.length" class="space-y-3">
        <li v-for="task in tasks" :key="task.id" class="p-4 bg-gray-100 rounded-lg shadow">
          <h3 class="text-lg font-bold text-gray-700"> {{ task.name }}</h3>
          <p class="text-gray-600">Description: {{ task.description }}</p>
          <button 
            @click="navigateToTaskDetails(task.id)" 
            class="mt-2 bg-call-to-action hover:bg-call-to-action-hover text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline"
          >
            View Details
          </button>
        </li>
      </ul>
      <div v-else class="text-gray-500">No tasks available for this drone.</div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import apiService from '@/services/apiService';
  
  const route = useRoute();
  const router = useRouter();
  const tasks = ref([]);
  const droneName = ref('');
  
  const fetchTaskDetails = async () => {
    const allTasks = await apiService.getTasks();
    const droneId = parseInt(route.params.id, 10);
    const drones = await apiService.getDrones();
    const selectedDrone = drones.find(drone => drone.id === droneId);
    droneName.value = selectedDrone ? selectedDrone.name : 'Unknown Drone';
  
    tasks.value = allTasks.filter(task => task.drone_id === droneId);
  };
  
  const navigateToTaskDetails = (taskId) => {
    router.push({ name: 'task-details', params: { id: taskId } });
  };
  
  onMounted(fetchTaskDetails);
  </script>
  