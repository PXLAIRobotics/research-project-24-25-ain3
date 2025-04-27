<template>
    <div class="interface">
        <navigationComponent />
        <chatComponent />
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import chatComponent from './ChatComponent.vue';
import navigationComponent from './NavigationComponent.vue';

// Router for navigation
const router = useRouter();

// Idle timeout value (default 120 seconds)
const idleTimeout = ref(120);
let timeoutId;

// Function to reset the timer (user activity detected)
function resetTimer() {
  clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    router.push('/'); // Redirect to landing page after inactivity
  }, idleTimeout.value * 1000); // Timeout in milliseconds
}

// Load the idleTimeout from localStorage if it exists
onMounted(() => {
  const storedTimeout = localStorage.getItem('idleTimeout');
  if (storedTimeout) {
    idleTimeout.value = parseInt(storedTimeout, 10);
  }

  // Setup event listeners to reset the timer on user interaction
  window.addEventListener('mousemove', resetTimer);
  window.addEventListener('keypress', resetTimer);
  window.addEventListener('click', resetTimer);
  window.addEventListener('scroll', resetTimer);

  // Start the first idle timeout countdown
  resetTimer();
});

// Cleanup event listeners when the component is unmounted
onUnmounted(() => {
  clearTimeout(timeoutId);
  window.removeEventListener('mousemove', resetTimer);
  window.removeEventListener('keypress', resetTimer);
  window.removeEventListener('click', resetTimer);
  window.removeEventListener('scroll', resetTimer);
});
</script>


<style>

</style>
