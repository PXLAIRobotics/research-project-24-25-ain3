<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router';
const router = useRouter();
import { useNavList } from '../stores/navList'
import NavigationItem from './NavigationItem.vue'


const navList = useNavList()

const conversations = computed(() => Object.values(navList.conversations))

const newConversation = () =>{
    window.location.reload();
}

const handleClick = () => {
  router.push({ name: 'adminComponent' });
};
</script>

<template>
    <v-card class="vCard">
        <v-layout>
            <v-navigation-drawer floating app>
                <v-list>
                    <v-list-item @click="handleClick" prepend-avatar="https://srcwap.com/wp-content/uploads/2022/08/abstract-user-flat-4.png" title="" class="vibe">
                      <span class="vibeTitle">VIBE</span>
                    </v-list-item>
                </v-list>

                <v-divider></v-divider>

                <v-list density="compact" nav>
                  <v-list-subheader class="faq-header">Frequently Asked Questions:</v-list-subheader>


                    <NavigationItem
                        v-for="conversation in conversations"
                        :key="conversation.id"
                        :conversation="conversation"/>
                </v-list>

                <v-list class="adminList">
                    <v-list-item>
                        <button class="NewConversation" @click="newConversation">New Chat</button>
                    </v-list-item>
                </v-list>

            </v-navigation-drawer>

        </v-layout>
    </v-card>
    <!-- <div class="Navigation">
        <h1>Vibe</h1>
        <button class="NewConversation" @click="navList.newConversation">New chat</button>
        <ul>
            <NavigationItem
            v-for="conversation in conversations"
            :key="conversation.id"
            :conversation="conversation"
            />
        </ul>
    </div> -->
</template>

<style scoped>
.vibe {
    height: 56px;
    display: flex;
    align-items: center;
    border-radius: 10px;
}

.vCard {
    background-color: #2a2a2a;
    z-index: 1;
}

v-navigation-drawer{
    overflow: hidden;
}

.vibeTitle {
    font-size: 18px;
    font-weight: bold;
    color: white;
    margin-right: 10px; /* Add spacing between the title and the button */
    white-space: nowrap; /* Prevent text wrapping */
}

.adminList {
    position: absolute;
    bottom: 10px; /* Keep the buttons at the bottom */
    width: 100%; /* Ensure it spans the width of the container */
    display: flex;
    justify-content: center;
    align-items: center;
}

.adminList v-list-item {
    display: flex;
    gap: 10px; /* Add spacing between the buttons */
    justify-content: center;
    width: 100%;
}

.NewConversation {
    color: #ffffff;
    padding: 10px 65px;
    border: none;
    cursor: pointer;
    border-radius: 5px;
    background-color: #680eee;
    text-align: center;
    white-space: nowrap;
    max-width: 100%;
}

.NewConversation:hover {
    background-color: #45087e;
}

/* Nav menu */
.Navigation {
    height: 100%;       /* 100% Full-height */
    width: 300px;       /* Decide width */
    position: fixed;    /* Stay in place */
    z-index: 1;         /* Stay on top */
    top: 0;             /* Stay at the top */
    left: 0;            /* Nav on left side */
    background-color: #2a2a2a;    /* Black*/
    overflow-x: hidden;             /* Disable horizontal scroll */
    padding-top: 60px;              /* Place content 60px from the top */
    transition: 0.5s;               /* 0.5 second transition effect to slide in the sidenav */
}

.Navigation div {
    margin: auto;
    width: 85%;
}

.faq-header {
  font-weight: bold;
  font-size: 14px;
  color: #ffffff;
  padding-left: 16px;
  padding-top: 12px;
}

/* Nav menu button for new chat */
.Navigation .newbtn {
    height: 40px;
    width: 120px;
    font-weight: bold;
    background-image: linear-gradient(to right, #c957b4, #395cdb);
    font-size: large;
    border: none;
    border-radius: 10px;
    color: white;
    cursor: pointer;
    margin: 30px 0px 25px 0px;
}

/* Title */
.Navigation h1 {
    color: white;
    position: absolute;
    top: 10px;
    margin: auto;
    font-size: 45px;
}

</style>
