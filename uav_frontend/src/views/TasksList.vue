<template>
  <div class="max-w-7xl mx-auto mt-10 p-5 bg-white shadow-lg rounded-lg">
    <div class="py-4">
      <h1 class="text-2xl font-semibold text-gray-900 text-center">Task Dashboard</h1>
    </div>
    <div class="flex flex-row justify-between items-center mb-8 px-8">
      <button @click="newTaskModal = true" class="mt-4 bg-positive-color hover:bg-positive-color-hover text-white font-bold py-2 px-4 rounded">
        Add Task
      </button>
      <input 
        v-model="searchTerm"
        type="text"
        placeholder="Search by drone name..."
        class="px-4 py-2 border rounded focus:outline-none focus:shadow-outline"
      />
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="task in filteredTasks" :key="task.id" class="bg-white p-4 shadow rounded-lg transition duration-300 ease-in-out transform hover:-translate-y-1 hover:shadow-lg">
        <h2 class="text-lg font-bold">{{ task.name }}</h2>
        <p class="text-gray-600">{{ task.description }}</p>
        <div>
          <button @click="selectTask(task.id)" class="mt-2 bg-call-to-action hover:bg-call-to-action-hover text-white font-bold py-2 px-4 rounded">
            View Details
          </button>
          <button
            @click="taskExecutionStatus[task.id] && taskExecutionStatus[task.id].success ? null : executeTask(task.id)"
            :class="taskExecutionStatus[task.id] && taskExecutionStatus[task.id].success ? 'bg-positive-color' : 'bg-warning-color hover:bg-warning-color-hover'"
            class="ml-2 text-white font-bold py-2 px-4 rounded relative cursor-pointer duration-300 ease-in-out"
            :disabled="taskExecutionStatus[task.id] && taskExecutionStatus[task.id].success"
          >
            <template v-if="taskExecutionStatus[task.id]?.loading">
            <span class="spinner"></span>
            </template>
            <template v-else-if="taskExecutionStatus[task.id]?.success">
              ✔ 
            </template>
            <template v-else-if="taskExecutionStatus[task.id]?.error">
              Try Again
            </template>
            <template v-else>
              Execute Task
            </template>
          </button>
          <button @click="deleteTask(task.id)" class="ml-2 bg-negative-color hover:bg-negative-color-hover text-white font-bold py-2 px-4 rounded duration-300 ease-in-out">
            Delete
          </button>
        </div>
      </div>
    </div>
    <transition name="fade">
      <div v-if="newTaskModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
        <form @submit.prevent="createTask" class="bg-white p-6 rounded shadow-lg">
          <div>
            <label for="name">Task Name:</label>
            <input v-model="newTask.name" id="name" required class="border p-2 rounded w-full">
          </div>
          <div class="mt-4">
            <label for="description">Description:</label>
            <textarea v-model="newTask.description" required id="description" class="border p-2 rounded w-full"></textarea>
          </div>
          <div class="mt-4">
            <label for="drone">Assign Drone:</label>
            <select v-model="newTask.drone_id" id="drone" required class="border p-2 rounded w-full">
              <option v-for="drone in drones" :value="drone.id" :key="drone.id">{{ drone.name }}</option>
            </select>
          </div>
          <div class="mt-4 text-right">
            <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
              Create Task
            </button>
            <button type="button" @click="newTaskModal = false" class="ml-2 bg-gray-300 hover:bg-gray-400 text-black font-bold py-2 px-4 rounded">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, reactive} from 'vue';
import apiService from '@/services/apiService';
import { useRouter } from 'vue-router';


const tasks = ref([]);
const drones = ref([]);
const router = useRouter();
const newTaskModal = ref(false);
const newTask = ref({ name: '', description: '', drone_id: '' });
const searchTerm = ref('');
const taskExecutionStatus = reactive({});

const initializeTaskStatuses = () => {
  const newStatuses = {};
  tasks.value.forEach(task => {
    if (task) { // Check task is not undefined
      newStatuses[task.id] = taskExecutionStatus[task.id] || {
        loading: false,
        success: task.is_executed,
        error: false
      };
    }
  });
  Object.keys(taskExecutionStatus).forEach(key => {
    if (!tasks.value.some(task => task.id.toString() === key)) {
      delete taskExecutionStatus[key]; // Clean up status of deleted tasks
    }
  });
  Object.assign(taskExecutionStatus, newStatuses);
};

onMounted(async () => {
  await fetchTasksAndDrones();
});

const fetchTasksAndDrones = async () => {
  tasks.value = await apiService.getTasks();
  drones.value = await apiService.getDrones();
  initializeTaskStatuses();
};



const createTask = async () => {
  const createdTask = await apiService.createTask(newTask.value);
  if (createdTask && createdTask.id) {
    tasks.value.push(createdTask);
    taskExecutionStatus[createdTask.id] = { loading: false, success: false, error: false };
    console.log(`Status initialized for new task with ID: ${createdTask.id}`);
  }
  newTaskModal.value = false;
  newTask.value = { name: '', description: '', drone_id: '' };
};


const executeTask = async (taskId) => {
  if (!taskExecutionStatus[taskId]) {
    console.error("Task status not initialized:", taskId);
    return;
  }
  const status = taskExecutionStatus[taskId];
  if (status.success) return;
  status.loading = true;
  status.error = false;
  try {
    await apiService.executeTask(taskId);
    status.success = true;
  } catch (error) {
    console.error('Error executing task:', error);
    status.error = true;
    status.success = false;
  } finally {
    status.loading = false;
  }
};

const selectTask = (taskId) => {
  router.push({ name: 'task-details', params: { id: taskId } });
};

const filteredTasks = computed(() => {
  if (!searchTerm.value) return tasks.value;
  return tasks.value.filter(task => {
    const drone = drones.value.find(d => d.id === task.drone_id);
    return drone ? drone.name.toLowerCase().includes(searchTerm.value.toLowerCase()) : false;
  });
});

const deleteTask = async (taskId) => {
  if (confirm("Are you sure you want to delete this task?")) {
    const response = await apiService.deleteTasks(taskId);
    if (response.message === "Task deleted successfully") {
      tasks.value = tasks.value.filter(task => task.id !== taskId);
      delete taskExecutionStatus[taskId];
      alert("Task deleted successfully.");
    } else {
      alert("Failed to delete the task.");
    }
  }
};
</script>

<style scoped>
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.spinner {
  display: inline-block;
  border: 2px solid #f3f3f3;  /* Light grey border */
  border-top: 2px solid #3498db;  /* Blue border top */
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
}
</style>