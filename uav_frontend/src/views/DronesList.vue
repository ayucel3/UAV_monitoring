<template>
  <div class="max-w-4xl mx-auto p-10 bg-white shadow-lg rounded-lg">
    <h1 class="text-xl text-center font-bold mb-4">Drones</h1>
    <ul class="space-y-4">
      <li v-for="drone in drones" :key="drone.id" @click="goToDroneDetails(drone.id)" class="flex justify-between items-center w-1/2 mx-auto py-2 border-solid hover:border-call-to-action border rounded-lg px-4 border-gray-200 cursor-pointer">
        {{ drone.name }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import apiService from '@/services/apiService';
import { useRouter } from 'vue-router';

const drones = ref([]);
const router = useRouter();

onMounted(async () => {
  drones.value = await apiService.getDrones();
});

const goToDroneDetails = (droneId) => {
  router.push({ name: 'drone-details', params: { id: droneId } });
};
</script>
