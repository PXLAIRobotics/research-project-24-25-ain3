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
            <v-navigation-drawer floating app expand-on-hover rail >
                <v-list>
                    <v-list-item prepend-avatar="https://srcwap.com/wp-content/uploads/2022/08/abstract-user-flat-4.png" title="VIBE" style="height: 56px; display: flex; align-items: center;">
                        <button prepend-icon="mdi-plus" class="NewConversation" @click="newConversation">Start new chat</button>
                    </v-list-item>
                </v-list>

                <v-divider></v-divider>

                <v-list density="compact" nav>
                    <NavigationItem
                        v-for="conversation in conversations"
                        :key="conversation.id"
                        :conversation="conversation"/>
                    
                    
                </v-list>
                
                <v-list class="adminList">
                    <v-list-item  >
                        <button class="adminButton" @click="handleClick">Admin Panel</button>
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
.vCard {
    background-color: #2a2a2a;
    z-index: 1;
}

v-navigation-drawer{
    overflow: hidden;
}

.NewConversation{
    background-color: #101010;
    padding: 3px;
    padding-left: 8px;
    padding-right: 8px;
    border-radius: 10px;
    margin-top: 4px;
    border: 1px solid rgb(164, 164, 164);
}

.adminButton{
    border: 1px solid rgb(164, 164, 164);
    background-color: #101010;
    padding: 3px;
    padding-left: 8px;
    padding-right: 8px;
    border-radius: 10px;
    
}

.adminList{
    position: absolute;
    bottom: 0;   
    margin-left: 45%;
    margin-bottom: 10px;
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