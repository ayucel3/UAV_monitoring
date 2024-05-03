import type { Drone, Task } from '@/services/types';

const baseUrl = 'http://localhost:5000/api';

async function getDrones(): Promise<Drone[]> {
  const response = await fetch(`${baseUrl}/drones`);
  return response.json();
}

async function getTasks(): Promise<Task[]> {
  const response = await fetch(`${baseUrl}/tasks`);
  return response.json();
}

async function createTask(task: Task): Promise<Task> {
  const response = await fetch(`${baseUrl}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(task),
  });
  return response.json();
}

async function getTaskDetails(taskId: number): Promise<Task> {
  const response = await fetch(`${baseUrl}/tasks/${taskId}`);
  return response.json();
}

async function executeTask(taskId: number): Promise<{ message: string }> {
  const response = await fetch(`${baseUrl}/tasks/${taskId}/execute`, { method: 'POST' });
  return response.json();
}

async function getImagesByTask(taskId: number): Promise<{ images: string[] }> {
  const response = await fetch(`${baseUrl}/tasks/${taskId}/images`);
  return response.json();
}

async function getAllImages(): Promise<{ images: string[] }> {
  const response = await fetch(`${baseUrl}/images`);
  return response.json();
}

async function deleteTasks(taskId: number): Promise<{ message: string }> {
  const response = await fetch(`${baseUrl}/tasks/${taskId}`, { method: 'DELETE' });
  return response.json();
}

export default {
  getDrones,
  getTasks,
  createTask,
  getTaskDetails,
  executeTask,
  getImagesByTask,
  getAllImages,
  deleteTasks,
};
