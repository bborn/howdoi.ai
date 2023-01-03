<script>
import * as htmlToImage from "html-to-image";
import { toPng, toJpeg, toBlob, toPixelData, toSvg } from "html-to-image";
const synth = window.speechSynthesis;
const speechRecognition = window.SpeechRecognition || webkitSpeechRecognition;

import hljs from "highlight.js";
import "highlight.js/styles/monokai-sublime.css";

let dummyPrompts = [
  {
    prompt: "Dummy Prompt",
    response: `1. This is a science question.
2. The answer to this question has to do with the Earth's orbit around the Sun and the tilt of the Earth's axis.
  <pre><code class="hljs language-javascript">
      function test() {
        alert('hi')
      }
    </code></pre>
4. As the Earth orbits the Sun, different parts of the Earth receive more or less direct sunlight, which causes the seasons.
5. During the summer, the northern hemisphere is tilted towards the Sun, and during the winter, the northern hemisphere is tilted away from the Sun.
6. This is why we have different seasons in different parts of the world.`,
  },
  { prompt: "Dummy Prompt", response: "Dummy response" },
  { prompt: "Dummy Prompt", response: "Dummy response" },
  { prompt: "Dummy Prompt", response: "Dummy response" },
  { prompt: "Dummy Prompt", response: "Dummy response" },
  { prompt: "Dummy Prompt", response: "Dummy response" },
];

export default {
  name: "App",
  props: {
    debug: {
      type: Boolean,
      default: import.meta.env.DEV,
    },
  },
  data() {
    let $this = this;
    return {
      listening: false,
      speaking: false,
      browserLanguage: navigator.language || navigator.userLanguage,
      recognition: null,
      focused: false,
      prompt: "",
      prompts: $this.debug ? dummyPrompts : [],
      selectedPromptIndex: null,
      loading: false,
      placeholderIndex: 0,
      placeholders: [
        "How do I get the interquartile range of a series of numbers?",
        "How do I find the median of a set of values?",
        "How do I prove that two angles are congruent?",
        "What is 2 + 2?",
        "What is the next number in the pattern: 3, 6, 9, 12, ___?",
        "How many sides does a triangle have?",
        "What is the difference between 15 and 7?",
        "What is the product of 5 and 6?",
        "What is the quotient of 18 divided by 3?",
        "What is the perimeter of a rectangle with sides that measure 5 and 8?",
        "What is the area of a circle with a radius of 4?",
        "What is the perimeter of a square with sides that measure 4?",
        "What is the volume of a rectangular prism with sides that measure 3, 4, and 5?",
        "What is the capital of the United States?",
        "How many planets are in our solar system?",
        "What is the biggest animal in the world?",
        "How do plants grow?",
        "What are the colors of the rainbow?",
        "How do babies grow inside their mother's belly?",
        "What is the highest mountain in the world?",
        "How do planes fly?",
        "What is the cycle of water?",
        "What are the different states of matter?",
        "Why do we have seasons?",
        "How do animals adapt to their environment?",
        "What is the food chain?",
        "What are the five senses?",
        "What is the difference between a plant and an animal?",
        "What is the function of the heart?",
        "What are the different parts of a flower?",
        "What are the different types of weather?",
        "What is the difference between a physical and a chemical change?",
        "What are the different types of rocks?",
        "How do I calculate the speed of an object?",
        "How do I determine the density of an object?",
        "How do I calculate the volume of an object?",
        "How do I find the force of friction on an object?",
        "How do I determine the amount of electrical current in a circuit?",
        "How do I calculate the power of an electrical device?",
        "How do I find the pitch of a sound wave?",
        "How do I calculate the wavelength of a wave?",
        "How do I determine the direction of a magnetic field?",
        "How do I find the strength of a magnet?",
        "How do I calculate the momentum of an object?",
        "How do I determine the amount of heat transferred in a system?",
        "How do I calculate the rate of work done by a force?",
        "How do I find the torque of a rotating object?",
        "How do I calculate the pressure of a fluid?",
        "How do I determine the amount of charge in an electrical circuit?",
        "How do I find the acceleration of an object?",
        "How do I calculate the force of gravity on an object?",
        "How do I determine the elasticity of an object?",
        "How do I research a historical event?",
        "How do I analyze primary and secondary sources?",
        "How do I create a timeline of events?",
        "How do I compare and contrast different historical perspectives?",
        "How do I use maps and other visual aids to understand history?",
        "How do I identify cause and effect in historical events?",
        "How do I evaluate the reliability of historical sources?",
        "How do I write a thesis statement for a history paper?",
        "How do I use evidence to support my arguments in history?",
        "How do I differentiate between fact and opinion in historical accounts?",
        "How do I understand the role of bias in historical interpretations?",
        "How do I identify and evaluate different interpretations of historical events?",
        "How do I understand the impact of historical events on different groups of people?",
        "How do I evaluate the importance of historical figures?",
        "How do I understand the connection between historical events and current events?",
        "How do I analyze the long-term consequences of historical events?",
        "How do I understand the role of technology in shaping historical events?",
        "How do I evaluate the significance of cultural, social, and economic factors in history?",
        "How do I analyze the impact of global interactions on historical events?",
        "How do I use critical thinking skills to evaluate historical information?",
      ],
    };
  },
  mounted() {
    // $(this.$refs.form).sticky();
    this.refreshPlaceholderIndex();
    this.higlightCode();
  },
  updated() {
    this.higlightCode();
    // hljs.highlightAll();
  },
  computed: {
    availableLanguages() {
      return [
        { name: "English", code: "en-US" },
        { name: "Spanish", code: "es-ES" },
        { name: "French", code: "fr-FR" },
      ];
    },
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
    stopSpeaking() {
      synth.cancel();
    },
    stopListening() {
      this.listening = false;
      this.recognition.stop();
    },
    listen() {
      if (this.listening) {
        this.stopListening();
        return;
      }
      synth.cancel();
      const $this = this;
      $this.listening = true;
      $this.recognition = new speechRecognition();
      $this.recognition.lang = $this.browserLanguage;

      $this.recognition.start();
      $this.recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        $this.prompt = transcript;
        $this.submitForm(transcript, true);
        $this.listening = false;
      };
    },
    speak(text, lang = "en-US") {
      if (this.speaking) {
        this.stopSpeaking();
        return;
      }
      this.speaking = true;

      const utterThis = new SpeechSynthesisUtterance(text);
      utterThis.addEventListener("end", () => {
        this.speaking = false;
      });

      const voices = synth.getVoices();

      for (const voice of voices) {
        if (!utterThis.voice) {
          console.log(voice.lang);
          if (voice.lang === lang) {
            utterThis.voice = voice;
            console.log(utterThis.voice.name);
          }
        }
      }

      console.log(lang);
      synth.speak(utterThis);
    },
    higlightCode() {
      document.querySelectorAll("pre code").forEach((el) => {
        hljs.highlightElement(el);
      });
    },
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
      // this.$refs.input.$el.focus();
      this.$refs.input.focus();
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
    submitForm(_event, speakResponse = false) {
      this.loading = true;
      fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: this.prompt,
          model: "text-davinci-003",
          temperature: 0.5,
          max_tokens: 512,
          history: this.prompts,
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          this.prompts.push({
            prompt: this.prompt,
            response: json.text,
            responseLanguage: json.language,
          });

          if (speakResponse) {
            this.speak(json.text, json.language);
          }

          this.prompt = "";
          this.loading = false;
          this.scrollToBottom();
        });
    },
  },
};
</script>

<template>
  <div class="ui">
    <div
      v-if="listening"
      class="ui active blurring page inverted content dimmer"
      @click="stopListening"
      style="z-index: 9999000"
    >
      <div class="content">
        <h2 class="ui inverted icon header">
          <i class="icon microphone" :class="{ red: listening }"></i>
        </h2>
      </div>
    </div>

    <div id="userInput" class="hover-parent">
      <div class="ui simple dropdown icon hovering" style="float: right">
        <i class="setting icon grey"></i>
        <div class="menu">
          <div class="header">
            <div class="ui form">
              <div class="field">
                <label for="">I speak:</label>
                <select v-model="browserLanguage" class="ui dropdown input">
                  <option value="en-US">English</option>
                  <option value="es-ES">Spanish</option>
                  <option value="fr-FR">French</option>
                  <option value="de-DE">German</option>
                  <option value="it-IT">Italian</option>
                  <option value="ja-JP">Japanese</option>
                  <option value="ko-KR">Korean</option>
                  <option value="pt-BR">Portuguese</option>
                  <option value="ru-RU">Russian</option>
                  <option value="zh-CN">Chinese</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
      <h1 class="ui page header">
        <a href="/">
          <span class="emoji">
            <em :data-emoji="shruggingType" class="medium"></em>
            <!-- <em data-emoji="shoulders" class="medium"></em> -->
          </span>

          <span class="text">howdoi.ai </span>
        </a>
      </h1>

      <form
        ref="form"
        @submit.prevent="submitForm"
        :class="{ loading }"
        class="ui huge form bottom"
      >
        <div class="field">
          <div class="ui right action left icon input">
            <i class="microphone icon link" @click="listen"></i>
            <input
              type="text"
              ref="input"
              @keydown.esc.stop.prevent="stopListening"
              @keydown.shift.space.exact.stop.prevent="listen"
              @keydown.tab="completePlaceholder"
              @keydown.meta.enter.exact.stop.prevent="submitForm"
              @keydown.enter.exact.stop.prevent="submitForm"
              @focus="focused = true"
              @blur="focused = false"
              :placeholder="prompts.length < 1 ? placeholder : ''"
              v-model="prompt"
            />

            <button type="submit" class="ui button primary">Go!</button>
          </div>

          <span class="ui small light grey text">
            <em v-if="focused && prompts.length < 1 && prompt == ''">
              Type a question, or hit 'tab' to try the sample prompt
            </em>
            <em v-else-if="focused">Enter to submit </em>
            <em v-else>&nbsp;</em>
          </span>
        </div>
      </form>
    </div>

    <div style="margin-top: 2em">
      <table
        v-if="prompts.length > 0"
        class="ui left aligned striped very relaxed table"
      >
        <template v-for="(prompt, index) in prompts">
          <tr class="prompt">
            <td class="collapsing">
              <em data-emoji=":thinking:" class="medium"></em>
            </td>
            <td>
              <p>
                <span v-html="prompt.prompt" class="ui large text"></span>
              </p>
            </td>
          </tr>
          <tr class="hover-parent response">
            <td class="collapsing top aligned">
              <em data-emoji=":robot:" class="medium"></em>
            </td>
            <td class="top aligned">
              <div>
                <p>
                  <span
                    v-html="prompt.response"
                    style="white-space: pre-line"
                    class="ui large text"
                  ></span>
                </p>

                <div style="float: right">
                  <a
                    href="#"
                    @click.stop.prevent="
                      speak(prompt.response, prompt.responseLanguage)
                    "
                    class="hovering ui icon button"
                  >
                    <i
                      class="ui icon"
                      :class="{
                        'volume up': !speaking,
                        'red play': speaking,
                      }"
                    ></i>
                  </a>

                  <a
                    :href="`mailto: feedback@howdoi.ai?subject=Feedback: ${prompt.prompt}&body=${prompt.response}`"
                    data-tooltip="Not a good answer?"
                    class="hovering ui icon button"
                  >
                    <i class="icon thumbs down"></i>
                  </a>
                </div>
              </div>
            </td>
          </tr>
        </template>
      </table>

      <button
        v-if="prompts.length > 0"
        @click="clearPrompts"
        class="ui tertiary icon button"
      >
        <i class="icon undo"></i>
        Start over
      </button>
    </div>
  </div>
</template>

<style>
iframe,
img {
  max-width: 100% !important;
}

pre {
  max-width: 100%;
  overflow: auto;
}
</style>

<style scoped>
p {
  line-height: 3em;
}

a.hovering,
.dropdown.hovering {
  visibility: hidden;
}

.hover-parent:hover a.hovering,
.hover-parent:hover .dropdown.hovering {
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

#userInput {
  position: sticky;
  top: 0px;
  z-index: 9999;
  padding-top: 2em;
  padding-bottom: 2em;
  background: #fff;
}

/* make the page header smaller on mobile devices */
@media only screen and (max-width: 767px) {
  .page.header span.text {
    font-size: 1.5em !important;
  }

  #userInput {
    padding-top: 1em;
    padding-bottom: 1em;
  }

  span.large.text {
    font-size: 1.2em !important;
  }

  em[data-emoji].medium {
    font-size: 1.5em !important;
  }

  table td.collapsing {
    display: inline !important;
    float: right;
  }
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

@keyframes rotate-think {
  30% {
    /* transform: rotate(-10deg); */
    transform: rotate3d(1, 0, 1, 25deg);

    /* transition-duration: 2000ms; */
    transition-timing-function: ease-in-out;
  }
  90% {
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
