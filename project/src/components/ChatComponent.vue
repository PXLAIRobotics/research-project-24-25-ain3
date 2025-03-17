<script setup>
import navigationComponent from './NavigationComponent.vue'
import { ref } from 'vue'
import axios from 'axios'

import standardGif from '@/assets/AI_Soundwave_standard.gif'
import transitionGif from '@/assets/AI_Soundwave_transition.gif'
import thinkingGif from '@/assets/AI_Soundwave_thinking.gif'

const currentGif = ref(standardGif)
const inputValue = ref('')
const messages = ref([])

const transitionDuration = 2500

const addMessage = (message, sender) => {
  messages.value.push({ sender: sender, message: message })
}

const sendMessage = () => {
  console.log('sendMessage called')
  currentGif.value = transitionGif

  setTimeout(() => {
    currentGif.value = thinkingGif
  }, transitionDuration)

  if (inputValue.value.trim() !== '') {
    addMessage(inputValue.value, 'client')

    axios
      .get('http://localhost:8000/pixie', {
        params: { message: inputValue.value },
      })
      .then((response) => {
        console.log(response.data)
        addMessage(response.data.data, 'chatbot')
      })
      .catch((error) => {
        console.error('Error:', error)
      })
  }

  inputValue.value = ''
}
</script>

<template>
  <div class="container">
    <div class="title">
      <h1>Corda</h1>
      <img class="logo" src="../assets/corda-logo.png" alt="corda logo" />
      <h1>Arena</h1>
    </div>

    <div class="chat-messages">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="msg.sender === 'client' ? 'clientMessage' : 'chatbotMessage'"
      >
        <p>{{ msg.message }}</p>
      </div>
    </div>

    <div class="circle">
      <img :src="currentGif" alt="standard soundwave" />
    </div>

    <div class="chatbox">
      <input v-model="inputValue" class="inputbox" type="text" placeholder="Message Vibe" @keyup.enter="sendMessage"/>
      <button class="sendbutton" @click="sendMessage">
        <img src="@/assets/send-icon.png" alt="send icon" class="image-button" />
      </button>
    </div>
  </div>
</template>



<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: black;
  height: 100%;
}

.title {
  position: absolute;
  margin: 5px;
  display: flex;
  flex-direction: row;
  top: 0;
}
.logo {
  width: 70px;
  height: 50px;
}

.circle {
  position: absolute;
  z-index: 0;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 250px;
  height: 250px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.circle img {
  height: 500px;
}

.chatbox {
  position: absolute;
  display: flex;
  flex-direction: row;
  width: 40%;
  margin: 20px;
  bottom: 20px;
}

.chatbox img {
  width: 20px;
}

.inputbox {
  background-color: #e0e0e0;
  width: 100%;
  border-radius: 20px;
  padding: 10px;
  border: none;
  color: black;
}

.inputbox::placeholder {
  color: black;
}

.sendbutton {
  background-color: transparent;
  border: none;
}

.sendbutton img {
  height: 30px;
  width: 30px;
}

.chat-messages {
  position: absolute;
  left: 27%;
  width: 46%;
  top: 12%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  z-index: 1;
  max-height: 500px;
  overflow-y: auto;
  margin-top: 20px;
}

.clientMessage {
  background-color: #e0e0e0;
  color: black;
  padding: 10px;
  border-radius: 15px;
  max-width: 300px;
  margin: 5px 0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  word-wrap: break-word;
  align-self: flex-end;
}

.chatbotMessage {
  background-color: #282727;
  color: rgb(235, 235, 235);
  padding: 10px;
  border-radius: 15px;
  max-width: 300px;
  margin: 5px 0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  word-wrap: break-word;
  display: flex;
}
</style>
