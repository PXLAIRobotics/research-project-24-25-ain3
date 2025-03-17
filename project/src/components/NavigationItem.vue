<script setup>
import { useNavList } from '../stores/navList'

defineProps({ conversation: { type: Object, required: true } })

const navList = useNavList()
</script>

<template>
  <v-list-item 
    
    class="NavigationItem" 
    :value="conversation.id" 
    @click="navList.openConversation(conversation.id)"
  >
    <!-- Prepend Icon (Fixed Issue) -->
    <template v-slot:prepend>
      <v-icon>mdi-message-outline</v-icon>
    </template>
    <v-list-item-content>
      <v-list-item-title>{{ conversation.title }}</v-list-item-title>
      <v-list-item-subtitle>{{ conversation.date }}</v-list-item-subtitle>
    </v-list-item-content>
  </v-list-item>
</template>

<style scoped>
/* Styling for subtitles (dates) */
.v-list-item-subtitle {
  color: white;
}

/* Nav menu links */
.NavigationItem {
  padding: 6px 6px 6px 16px;
  text-decoration: none;
  font-size: 20px;
  color: #818181;
  display: block;
  transition: 0.3s;
  text-align: left;
  border-radius: 10px;
  width: 100%;
  margin: auto;
}

/* Change color when hovering over nav link */
.NavigationItem:hover {
  color: #f1f1f1;
}
</style>