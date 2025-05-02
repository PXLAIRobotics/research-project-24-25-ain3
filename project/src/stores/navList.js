import { defineStore } from 'pinia'

export const useNavList = defineStore('navList', {
    // Default state
    state: () => {
        return {
            conversations: {
                faq1: {
                    id: "1",
                    question: "Wat is de Corda Arena?",
                    answer: "De Corda Arena is een innovatieve evenementenlocatie op de Corda Campus in Hasselt. Met een oppervlakte van 10.000 m² en een hoogte van 24 meter biedt de arena plaats aan maximaal 3.750 bezoekers. Daarnaast kunnen miljoenen mensen virtueel deelnemen via geavanceerde streaming- en holografische technologieën."
                },
                faq2: {
                    id: "2",
                    question: "Welke soorten evenementen kunnen plaatsvinden in de Corda Arena?",
                    answer: "De Corda Arena is geschikt voor een breed scala aan evenementen, waaronder concerten, sportevenementen, beurzen, conferenties en andere grootschalige bijeenkomsten. De flexibele indeling en moderne faciliteiten maken het mogelijk om elk type evenement te organiseren."
                },
                faq3: {
                  id: "3",
                  question: "Wat is de maximale capaciteit van de arena?",
                  answer: "De Corda Arena heeft een maximale capaciteit van 3.750 bezoekers voor live evenementen. Dit aantal kan variëren afhankelijk van de opstelling en het type evenement dat wordt georganiseerd."
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
