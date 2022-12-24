<script>
import Editor from "./components/Editor.vue";

const OPENAI_API_KEY = import.meta.env.VITE_OPENAI_API_KEY;

import * as htmlToImage from "html-to-image";
import { toPng, toJpeg, toBlob, toPixelData, toSvg } from "html-to-image";

let dummyPrompts = [{ prompt: "Dummy Prompt", response: "Dummy response" }];

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
    let $this = this;
    return {
      loading: false,
      content: `
        <p>But as she gets to know Alex better, Emma realizes that he sees her in a way that no one else ever has. He appreciates her for who she is, and he encourages her to pursue her dreams and follow her heart.</p>
        <p>As they spend more time together, Alex and Emma's love for each other deepens. And on a starry night in the park, surrounded by the twinkling lights of the city, Alex proposes to Emma.</p>`,
    };
  },
  mounted() {},
  computed: {
    selectedPrompt() {
      return this.prompts[this.selectedPromptIndex];
    },
    shruggingType() {
      let types = [
        ":person_shrugging:",
        ":person_shrugging_tone1:",
        ":person_shrugging_tone2:",
        ":person_shrugging_tone3:",
        ":person_shrugging_tone4:",
        ":person_shrugging_tone5:",
        ":woman_shrugging:",
        ":woman_shrugging_tone1:",
        ":woman_shrugging_tone2:",
        ":woman_shrugging_tone3:",
        ":woman_shrugging_tone4:",
        ":woman_shrugging_tone5:",
      ];
      var randomIndex = Math.floor(Math.random() * types.length);
      var randomElement = types[randomIndex];

      return randomElement;
    },
    placeholder() {
      var randomElement = this.placeholders[this.placeholderIndex];

      return randomElement;
    },
  },
  methods: {
    shareResponse(promptObject) {
      let $this = this;
      let prompt = `🤔 ${promptObject.prompt}`;

      let lines = promptObject.response.split("\n");
      let trimmedLines = lines.map((line) => line.trimStart());

      let response = `🤖\n${trimmedLines.join("\n")}`;
      let url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(
        prompt
      )}%0A%0A${encodeURIComponent(response)}%0Awww.howdoi.ai`;
      window.open(url, "_blank");
    },
    downloadResponseAsJpeg(promptIndex) {
      this.selectedPromptIndex = promptIndex;

      this.$nextTick(() => {
        let element = this.$refs.currentPromptElement;

        htmlToImage
          .toJpeg(element, {
            backgroundColor: "#ffffff",
          })
          .then(function (dataUrl) {
            var link = document.createElement("a");
            link.download = "prompt.jpeg";
            link.href = dataUrl;
            link.click();
          });
      });
    },
    scrollToBottom() {
      this.$nextTick(() => {
        var promptElements = document.querySelectorAll(".prompt");
        if (promptElements.length > 0) {
          promptElements[promptElements.length - 1].scrollIntoView();
        }
      });
    },
    refreshPlaceholderIndex() {
      var randomIndex = Math.floor(Math.random() * this.placeholders.length);
      this.placeholderIndex = randomIndex;
      this.$refs.input.$el.focus();
    },
    completePlaceholder() {
      if (this.prompt == "") {
        this.prompt = this.placeholder;
        this.submitForm();
      }
    },
    clearPrompts() {
      this.prompts = [];
    },
    submitForm() {
      this.loading = true;
      fetch("/assist", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${OPENAI_API_KEY}`,
        },
        body: JSON.stringify({
          prompt: `
              Q: ${this.prompt}\n
              First, determine what topic this question is about
              (for example, is it a math question, a history question, a science question, or some other topic?).

              If it's a math question, then evaluate what kind of question it is (for example, is it a word problem, a logic problem, a proof, or an algebra problem).

              Return your answer as a list of steps.\n

              A: Let's think through the answer step by step:\n
            `,
          model: "text-davinci-003",
          temperature: 0.5,
          max_tokens: 512,
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          this.prompts.push({
            prompt: this.prompt,
            response: json.choices[0].text,
          });
          this.prompt = "";
          this.loading = false;
          this.scrollToBottom();
        });
    },
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

a.hovering {
  visibility: hidden;
}

.hover-parent:hover a.hovering {
  visibility: visible;
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

em[data-emoji="shoulders"]:before {
  background-image: url(./assets/shoulders.svg);
}

h1:hover em:before {
  animation: grow-shrink 500ms 1;
}

textarea.resize {
  border-top-right-radius: 0 !important;
  border-bottom-right-radius: 0 !important;
}

/* h1 span.emoji {
  position: relative;
  
}

h1 span.emoji em {
  position: absolute;
  top: 0;
  left: 0;
} */

@keyframes rotate-think {
  0% {
    /* transform: rotate(-10deg); */
    transform: rotate3d(1, 0, 1, 125deg);
    /* transition-duration: 2000ms; */
    transition-timing-function: ease-in-out;
  }
  20% {
    transform: rotate(0deg);
    /* transition-duration: 200ms; */
    transition-timing-function: ease-in-out;
  }
}

tr:hover em[data-emoji=":thinking:"]:before {
  animation: rotate-think 2s 1;
}

tr:hover em[data-emoji=":robot:"]:before {
  animation: grow-shrink 500ms 1;
}
</style>
