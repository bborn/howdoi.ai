import { createApp } from 'vue'
import Write from './Write.vue'
import Chat from './Chat.vue'


import './assets/main.css'

import ResizeTextarea from "resize-textarea-vue3";

createApp(Write).mount('#write')

createApp(Chat).mount('#chat')

