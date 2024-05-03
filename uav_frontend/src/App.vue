<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="sticky top-0 left-0 right-0 bg-primary-color text-white flex items-center justify-center p-4">

    <nav>
      <RouterLink class="text-call-to-action mx-2 hover:text-call-to-action-hover" to="/">Home</RouterLink>
      <RouterLink class="text-call-to-action mx-2 hover:text-call-to-action-hover" to="/drones">Drones</RouterLink>
      <RouterLink class="text-call-to-action mx-2 hover:text-call-to-action-hover" to="/tasks">Tasks</RouterLink>
    </nav>
  </header>

  <main class="bg-primary-color ">
    <RouterView />
  </main>
</template>
