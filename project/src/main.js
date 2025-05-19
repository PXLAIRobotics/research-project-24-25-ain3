import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: 'dark', 
      },
}
)


const app = createApp(App)

app.use(createPinia())
//app.use(router)

app.mount('#app')

import router from './router' // Correctly import the router

createApp(App).use(router).use(vuetify).mount('#app')

