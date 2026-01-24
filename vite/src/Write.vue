<script>
import Editor from "./components/Editor.vue";
import * as htmlToImage from "html-to-image";

export default {
  name: "App",
  components: {
    Editor,
  },
  props: {
    debug: {
      type: Boolean,
      default: import.meta.env.DEV,
    },
  },
  data() {
    return {
      loading: false,
      content: `
        <p>But as she gets to know Alex better, Emma realizes that he sees her in a way that no one else ever has. He appreciates her for who she is, and he encourages her to pursue her dreams and follow her heart.</p>
        <p>As they spend more time together, Alex and Emma's love for each other deepens. And on a starry night in the park, surrounded by the twinkling lights of the city, Alex proposes to Emma.</p>`,
    };
  },
  methods: {
    downloadResponseAsJpeg(promptIndex) {
       // This functionality seems tied to the old prompt system but htmlToImage is imported
       // Leaving it if needed for future extension, but cleaning up the prompt-specific logic
    }
  },
};
</script>

<template>
  <div class="ui basic segment">
    <h1>Write</h1>
    <editor v-model="content" />
  </div>
</template>

<style scoped>
p {
  line-height: 3em;
}

h1:hover em:before {
  animation: grow-shrink 500ms 1;
}

@keyframes grow-shrink {
  0% {
    transform: scaleY(1);
    transform-origin: bottom;
    transition-duration: 0.2ms;
    transition-timing-function: ease-in-out;
  }
  20% {
    transform: scaleY(1.05);
    transform-origin: bottom;
    transition-duration: 0.2ms;
    transition-timing-function: ease-in-out;
  }
  40% {
    transform: scaleY(1);
    transform-origin: bottom;
  }
  60% {
    transform: scaleY(1.05);
    transform-origin: bottom;
  }
  80% {
    transform: scaleY(1);
    transform-origin: bottom;
  }
}

.page.header span.text {
  font-family: "Fredoka One", cursive !important;
  font-size: 2em !important;
  letter-spacing: 2px;
  vertical-align: bottom;
  line-height: 1em;
  background: linear-gradient(to right, #333 75%, #ccc 70%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>