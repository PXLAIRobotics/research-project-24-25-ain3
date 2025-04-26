<template>
  <div class="centered-container">
    <img
      src="../assets/AI_Soundwave_standard.gif"
      alt="Clickable Image"

      @click="handleClick"
      class="clickable-image"
    >
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const handleClick = () => {
  router.push({ name: 'interfaceComponent' });
};

</script>

<style scoped>
.centered-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.clickable-image {
  cursor: pointer;
}
</style>
