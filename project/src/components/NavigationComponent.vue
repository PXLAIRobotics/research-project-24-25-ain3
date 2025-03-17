<script setup>
import { computed } from 'vue'
import { useNavList } from '../stores/navList'
import NavigationItem from './NavigationItem.vue'

const navList = useNavList()

const conversations = computed(() => Object.values(navList.conversations))

</script>

<template>
    <v-card class="vCard">
        <v-layout>
            <v-navigation-drawer expand-on-hover rail >
                <v-list>
                    <v-list-item prepend-avatar="https://srcwap.com/wp-content/uploads/2022/08/abstract-user-flat-4.png" title="VIBE">
                        
                    </v-list-item>
                </v-list>

                <v-divider></v-divider>

                <v-list density="compact" nav>
                    <NavigationItem
                        v-for="conversation in conversations"
                        :key="conversation.id"
                        :conversation="conversation"/>
                    
                    <v-list-item prepend-icon="mdi-folder" title="My Files" value="myfiles"></v-list-item>
                    <v-list-item prepend-icon="mdi-account-multiple" title="Shared with me" value="shared"></v-list-item>
                    <v-list-item prepend-icon="mdi-star" title="Starred" value="starred"></v-list-item>
                </v-list>
                <v-button>
                    
                </v-button>
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
.vCard {
    background-color: #2a2a2a;
}

v-navigation-drawer{
    overflow: hidden;
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