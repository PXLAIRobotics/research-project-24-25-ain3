<script setup>
import { useNavList } from '../stores/navList'

defineProps({ conversation: { type: Object, required: true } })

const navList = useNavList()
</script>

<template>
    <li class="NavigationItem">
        <h2>{{ conversation.date }}</h2>
        <a href="#" @click="navList.openConversation(conversation.id)">{{ conversation.title }}</a>
    </li>
</template>

<style scoped>
/* Date for older chats */ 
.item h2 {
    color: white;
}

/* Nav menu links */
.item a {
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
.item a:hover {
    color: #f1f1f1;
}
</style>