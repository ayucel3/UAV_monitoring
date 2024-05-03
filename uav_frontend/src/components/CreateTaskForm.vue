<template>
    <div class="max-w-md mx-auto p-4">
      <form @submit.prevent="submitTask">
        <div class="mb-4">
          <label for="name" class="block text-sm font-medium text-gray-700">Task Name</label>
          <input type="text" id="name" v-model="task.name" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" placeholder="Enter task name">
        </div>
        <div class="mb-4">
          <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
          <textarea id="description" v-model="task.description" rows="3" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" placeholder="Enter task description"></textarea>
        </div>
        <div class="mb-4">
          <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Create Task</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import apiService from '@/services/apiService';
  
  const task = ref({
    name: '',
    description: ''
  });
  
  const submitTask = async () => {
    await apiService.createTask(task.value);
    alert('Task created successfully!');
    task.value = { name: '', description: '' }; 
  };
  </script>
  