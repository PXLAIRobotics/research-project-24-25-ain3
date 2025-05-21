<template>
  <div class="facial-recognition-container">
    <div class="video-container">
      <video ref="video" width="640" height="480" autoplay muted></video>
    </div>
    <div v-if="isProcessing" class="overlay">
      <p>Processing...</p>
    </div>
    <div v-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
    </div>
    <button @click="cancelRecognition" class="cancel-btn">Cancel</button>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'

const emit = defineEmits(['authenticated', 'cancel'])

const video = ref(null)
const isProcessing = ref(false)
const errorMessage = ref('')
let detectionInterval = null

const startVideo = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: {} })
    video.value.srcObject = stream
  } catch (err) {
    errorMessage.value = 'Error accessing webcam'
    console.error(err)
  }
}

// Take a snapshot from video
const captureSnapshot = () => {
  const canvas = document.createElement('canvas')
  canvas.width = video.value.videoWidth
  canvas.height = video.value.videoHeight
  const ctx = canvas.getContext('2d')
  ctx.drawImage(video.value, 0, 0)
  return canvas.toDataURL('image/jpeg') // returns base64
}

// Send image to backend
const sendToBackend = async () => {
  isProcessing.value = true
  errorMessage.value = ''

  const base64Image = captureSnapshot()

  try {
    const response = await axios.post('http://localhost:8000/facial-login', {
      image: base64Image
    })

    const label = response.data.label
    if (label) {
      emit('authenticated', label)
    } else {
      errorMessage.value = 'Face not recognized'
    }
  } catch (err) {
    console.error(err)
    errorMessage.value = 'Error sending image to backend'
  }

  isProcessing.value = false
}

const cancelRecognition = () => {
  emit('cancel')
}

onMounted(async () => {
  await startVideo()
  detectionInterval = setInterval(sendToBackend, 2000) // Every 2 sec
})

onBeforeUnmount(() => {
  if (video.value && video.value.srcObject) {
    video.value.srcObject.getTracks().forEach(track => track.stop())
  }
  clearInterval(detectionInterval)
})
</script>


<style scoped>
.facial-recognition-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.7);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
}

.video-container {
  margin-bottom: 20px;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.error-message {
  color: red;
  font-size: 1.2em;
}

.cancel-btn {
  background-color: #ff6666;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
}

.cancel-btn:hover {
  background-color: #ff4c4c;
}
</style>
