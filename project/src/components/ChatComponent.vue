<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { marked } from 'marked';

import { watch } from 'vue'
import { useNavList } from '../stores/navList'


import standardGif from '@/assets/AI_Soundwave_standard.gif'
import transitionGif from '@/assets/AI_Soundwave_transition.gif'
import thinkingGif from '@/assets/AI_Soundwave_thinking.gif'

const currentGif = ref(standardGif)
const inputValue = ref('')
const messages = ref([])
const chatDisabled = ref(false)
const endChatMessage = ref('')
const audioUrl = ref('')
const mediaRecorder = ref(null);
let chunks = [];
const isRecording = ref(false)
const isTtsStarted = ref(false);
const navList = useNavList()


const transitionDuration = 2500

const toggleRecording = async () => {
  if (isRecording.value) {
    await stopRecording()
  } else {
    await startRecording()
  }
}


const addMessage = (message, sender) => {
  messages.value.push({ sender: sender, message: message })
}

const routeMessage = () =>{
  inputValue.value = `Wat is de route van [Huidige locatie] naar [Eindbestemming]`;
}

const sendMessage = () => {
  console.log('sendMessage called');
  currentGif.value = transitionGif;

  setTimeout(() => {
    currentGif.value = thinkingGif;
  }, transitionDuration);

  if (inputValue.value.trim() !== '') {
    addMessage(inputValue.value, 'client');

    const typingMessage = { sender: 'chatbot', message: '...' };
    messages.value.push(typingMessage);

    const userMessage = inputValue.value;
    inputValue.value = '';

    axios
      .get('http://localhost:8000/pixie', {
        params: { message: userMessage },
      })
      .then((response) => {
        const chatbotMessage = marked(response.data.data);
        
        // 🔊 TTS hier uitvoeren
        const plainText = response.data.data
          .replace(/<[^>]*>/g, '')         // Verwijdert HTML-tags
          .replace(/[\r\n]+/g, '. '); // punten ipv doorlopende tekst
        // Start de TTS pas af wanneer we de chatbotmessage kunnen tonen
        axios
          .get('http://localhost:8000/tts', {
            params: { text: plainText },
            responseType: 'blob'
          })
          .then((response) => {
            // Maak een blob van het audiobestand
            const blob = new Blob([response.data], { type: 'audio/mp3' });
            const url = URL.createObjectURL(blob);
            audioUrl.value = url;

            // Speel de audio af
            const audio = new Audio(url);

            audio.play().then(() => {
              console.log('Audio is playing');
              isTtsStarted.value = true; // Markeer dat de TTS is gestart
              const index = messages.value.findIndex(msg => msg.message === '...');
              if (index !== -1) {
                messages.value.splice(index, 1);
              }

              // Voeg de chatbot message pas toe als de TTS is begonnen
              addMessage(chatbotMessage, 'chatbot');
            }).catch(error => {
              console.error('Error playing audio:', error);
              alert('Er is een fout opgetreden bij het afspelen van de audio.');
            });
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('Er is een fout opgetreden bij het ophalen van de spraak.');
          });

        if (response.data.endChat !== "") {

          chatDisabled.value = true;
          endChatMessage.value = response.data.endChat;
          addMessage(endChatMessage.value, 'chatbot');
        }
      })
      .catch((error) => {
        console.error('Error:', error);

        const index = messages.value.findIndex(msg => msg.message === '...');
        if (index !== -1) {
          messages.value.splice(index, 1);
        }

        addMessage('Er is een fout opgetreden. Probeer het later opnieuw.', 'chatbot');
      });
  }

  inputValue.value = '';
};



const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder.value = new MediaRecorder(stream)
    chunks.length = 0 // reset chunks

    mediaRecorder.value.ondataavailable = e => {
      if (e.data.size > 0) chunks.push(e.data)
    }

    mediaRecorder.value.onstop = async () => {
      const blob = new Blob(chunks, { type: 'audio/webm' })
      chunks.length = 0

      const formData = new FormData()
      formData.append('audio', blob, 'speech.webm')

      try {
        const res = await fetch('http://localhost:8000/transcribe', {
          method: 'POST',
          body: formData,
        })

        const data = await res.json()
        if (data.text) {
          console.log('Transcript:', data.text)
          inputValue.value = data.text
          sendMessage()
        } else {
          alert('Geen tekst herkend.')
        }
      } catch (err) {
        console.error('Transcribe error:', err)
        alert('Fout bij spraakherkenning.')
      }
    }

    mediaRecorder.value.start()
    isRecording.value = true
  } catch (err) {
    console.error('Microfoon toegang geweigerd of niet beschikbaar.', err)
    alert('Microfoon niet beschikbaar of geweigerd.')
  }
}

const stopRecording = async () => {
  if (mediaRecorder.value && mediaRecorder.value.state !== 'inactive') {
    mediaRecorder.value.stop()
    isRecording.value = false
  }
}


watch(
  () => navList.activeQA,
  (qa) => {
    if (qa) {
      addMessage(qa.question, 'client')
      addMessage(qa.answer, 'chatbot')
      navList.clearActiveQA()
    }
  }
)
</script>

<template>
  <div class="container">
    <header>
      <div class="title">
        <h1>Corda</h1>
        <img class="logo" src="../assets/corda-logo.png" alt="corda logo" />
        <h1>Arena</h1>
      </div>
    </header>


    <div class="chat-messages">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="msg.sender === 'client' ? 'clientMessage' : 'chatbotMessage'"
      >
        <p v-html="msg.message"></p>
      </div>
    </div>

    <div class="circle">
      <img :src="currentGif" alt="standard soundwave" />
    </div>

    <div class="chatbox">
      <button class="routeButton" @click="routeMessage" :disabled="chatDisabled">Route Vragen</button>
      <input v-model="inputValue" class="inputbox" type="text" placeholder="Message Vibe" @keyup.enter="sendMessage" :disabled="chatDisabled"/>
      <button @click="toggleRecording" class="sendbutton" :class="{ recording: isRecording }" :disabled="chatDisabled" > 
        <img src="@/assets/sound-waves.png" alt="speak icon" class="speak-image" /> 
      </button>
    </div>
  </div>
</template>



<style scoped>

header{
  display: flex;
  justify-content: center;  /* Center children horizontally */
  align-items: center;      /* Center children vertically */
  background-color: #212121;
  position: absolute;
  top: 0;
  width: 100%;              /* Make header span full width */
  padding: 10px 0;
  z-index: 0;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #333333;
  height: 100%;
}

.title {
  display: flex;
  flex-direction: row;
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
  opacity: 0.5;
}

.chatbox {
  position: absolute;
  display: flex;
  flex-direction: row;
  width: 45%;
  margin: 20px;
  bottom: 20px;
  height: 50px;
}

.chatbox img {
  width: 20px;
}

.inputbox {
  background-color: #e0e0e0;
  width: 100%;
  border-radius: 20px;
  padding: 0 0 0 15px;
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
  height: 40px;
  width: 40px;
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

  list-style-type: disc;

}

.clientMessage {
  background-color: #e0e0e0;
  color: black;
  padding: 10px;
  border-radius: 15px;
  max-width: 300px;
  margin: 5px 10px 0 0;
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
  margin: 5px 0 0px 30px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  word-wrap: break-word;
  display: flex;
}

:deep(.chat-messages ul) {
    padding-left: 40px !important;
}

.routeButton{
  background-color: #e0e0e0;
  margin-right: 20px;
  color: black;
  padding: 0 10px 0 10px;
  width: 180px;
  border-radius: 20px;
  height: 45px;
  margin-top: px;

}

.inputbox:disabled {
  background-color: #bdbdbd;
  cursor: not-allowed;
}

.sendbutton:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.routeButton:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}


.speak-image{
  background-color: white;
  height: 40px;
  margin: 0;
  border-radius: 20px;
  padding: 5px;
}

.sendbutton.recording .speak-image {
  background-color: #2196f3; /* blauw */
}
</style>
