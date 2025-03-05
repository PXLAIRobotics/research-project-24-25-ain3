<template>
    <div class="container">
        
        <div class="title">
            <h1>Corda</h1>
            <img class="logo" src="../assets/corda-logo.png" alt="corda logo">
            <h1>Arena</h1>
        </div>

        <div class="chat-messages">
            <div v-for="(msg, index) in messages" :key="index" class="message-bubble">
                <p>{{ msg }}</p>
            </div>
        </div>

        <div class="circle">
            <img :src="currentGif" alt="standard soundwave">
        </div>

        <div class="chatbox">
            <input v-model="inputValue" class="inputbox" type="text" placeholder="Message Vibe" />
            <button class="sendbutton" @click="sendMessage">
                <img src="@/assets/send-icon.png" alt="send icon" class="image-button" />
            </button>
        </div>

        
    </div>
    
</template>

<script setup>
import { ref } from 'vue';

import standardGif from '@/assets/AI_Soundwave_standard.gif';
import transitionGif from '@/assets/AI_Soundwave_transition.gif';
import thinkingGif from '@/assets/AI_Soundwave_thinking.gif';

const currentGif = ref(standardGif);
const inputValue = ref('');
const messages = ref([]);

const transitionDuration = 2500; 

const sendMessage = () => {

  currentGif.value = transitionGif;

  setTimeout(() => {
    currentGif.value = thinkingGif;
  }, transitionDuration); 

  if (inputValue.value.trim() !== '') {
    messages.value.push(inputValue.value);
  }

  inputValue.value = '';
};
</script>

<style scoped>
    .container{
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: black;
        height: 100%;
    }

    .title{
        position: absolute;
        z-index: -1; 
        margin: 5px;
        display: flex;
        flex-direction: row;
        top: 0;
    }
    .logo{
        width: 70px;
        height: 50px;
    }

    .circle{
        position: absolute;
        z-index: -1; 
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 250px; 
        height: 250px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .circle img{
       height: 500px;
    }

    .chatbox{
        position: absolute; 
        display: flex;
        flex-direction: row;
        width: 40%;
        margin: 20px;
        bottom: 20px;
    }

    .chatbox img{
        width: 20px;
        
    }

    .inputbox{
        background-color: #e0e0e0;
        width: 100%;
        border-radius: 20px;
        padding: 10px;
        border: none;
        color: black;
    }

    .inputbox::placeholder{
        color: black;
    }

    .sendbutton{
        background-color: transparent;
        border: none;
    }

    .sendbutton img{
        height: 30px;
        width: 30px;
    }

    .chat-messages {
        position: absolute;
        right: 30%;
        top: 12%;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        justify-content: flex-start;
        width: 100%;
        max-height: 500px;
        overflow-y: auto;
        margin-top: 20px;
    }

    .message-bubble {
        background-color: #e0e0e0;
        color: black;
        padding: 10px;
        border-radius: 15px;
        max-width: 300px;
        margin: 5px 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        word-wrap: break-word;
    }


   
    
</style>