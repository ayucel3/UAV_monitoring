<template>
    <div class="max-w-4xl mx-auto mt-10 p-5 bg-white shadow-lg rounded-lg">
        <div class="grid grid-cols-2">
            <div class="col-span-1">
                <h1 class="text-2xl font-bold mb-4">{{ task.name }}</h1>
                <p class="mb-4">{{ task.description }}</p>
            </div>
            <div class="col-span-1 items-center text-end">
                <div v-if="task.isExecuted">
                    <span class="text-green-500 font-bold">Successfully Executed</span>
                </div>
                <button v-else @click="executeTask" class="bg-call-to-action hover:bg-call-to-action-hover text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline">
                    Execute Task
                </button>
            </div>
        </div>
      <div v-if="images.length > 0" class="mt-4">
        <h2 class="text-lg font-bold mb-3">Images</h2>
        <div class="grid grid-cols-3 gap-4">
          <img v-for="image in images" :src="`data:image/png;base64,${image}`" alt="Task Image" :key="image" class="max-w-full h-auto shadow-lg rounded">
        </div>
      </div>
    </div>
  </template>
  
  
  <script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import apiService from '@/services/apiService';

const route = useRoute();
const task = ref({});
const images = ref([]);

const fetchTaskDetails = async () => {
  const details = await apiService.getTaskDetails(route.params.id);
  task.value = {...details, isExecuted: details.is_executed || false};
  if (task.value.isExecuted) {
    fetchImages();
  }
};

const fetchImages = async () => {
  const response = await apiService.getImagesByTask(route.params.id);
  images.value = response.images;
};

onMounted(fetchTaskDetails);

const executeTask = async () => {
  const result = await apiService.executeTask(task.value.id);
  if (result.message === 'Task executed and images captured') {
    task.value.isExecuted = true; 
    fetchImages();
  }
};
</script>
