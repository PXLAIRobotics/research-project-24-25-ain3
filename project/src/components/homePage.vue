<template>
    <div class="centered-container">
      <img 
        src="../assets/output-onlinegiftools.gif" 
        alt="Clickable Image" 
        @click="handleClick"
        class="clickable-image"
      >
    </div>
  </template>
  
  <script setup>
  const handleClick = () => {
    alert("Image Clicked!"); 
  };
  </script>
  
  <style scoped>
  .centered-container {
    margin-left: auto;
    margin-right: auto;
    max-width: fit-content;
  }
  
  .clickable-image {
    cursor: pointer; 
  }
  </style>
  