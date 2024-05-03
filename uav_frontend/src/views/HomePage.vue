<template>
  <div class="min-h-[80vh] bg-primary-color flex flex-col justify-center items-center text-center px-4">
    <h1 class="text-4xl font-bold text-gray-800 mb-2">
      Welcome to the UAV Monitoring Platform
    </h1>
    <p class="text-lg text-gray-600">
      Created By Aral Yucel
    </p>
    <div class="mt-6 flex flex-row justify-center gap-4">
      <router-link to="/drones" class="bg-call-to-action hover:bg-call-to-action-hover text-white font-bold py-2 px-4 rounded-full">
        Manage Drones
      </router-link>
      <router-link to="/tasks" class="hover:bg-call-to-action-hover border border-solid border-call-to-action text-black hover:text-white hover:border-black font-bold py-2 px-4 rounded-full">
        Manage Tasks
      </router-link>
    </div>
  </div>
</template>