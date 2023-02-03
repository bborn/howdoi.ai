import { createApp } from 'vue'
import Write from './Write.vue'
import Chat from './Chat.vue'


import './assets/main.css'

import ResizeTextarea from "resize-textarea-vue3";

createApp(Write).mount('#write')

const mountEl = document.querySelector("#chat");
createApp(Chat, { ...mountEl.dataset }).mount('#chat')

