import { defineStore } from 'pinia'

export const useNavList = defineStore('navList', {
    // Default state
    state: () => {
        return {
            conversations: {
                lastWeek: {
                    id: "1",
                    date: "03/03/2025",
                    title: "Convo1"
                },
                today: {
                    id: "1",
                    date: "Today",
                    title: "Convo"
                }
            }
        }
    },
    actions: {
        newConversation() {
            // TO DO
        },
        openConversation(conversationID) {
            // TO DO
        }
    }
}
)