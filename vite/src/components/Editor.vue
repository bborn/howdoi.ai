<template>
  <div class="">
    <div v-if="editor">
      <bubble-menu
        class="ui inverted menu"
        :tippy-options="{ duration: 100 }"
        :editor="editor"
      >
        <a @click="editor.chain().focus().gpt().run()" class="icon item">
          <i class="icon magic wand"></i>
        </a>
      </bubble-menu>
    </div>

    <div
      v-if="editor"
      class="ui top attached menu stackable"
      :class="{ disabled: loading }"
    >
      <a
        class="item"
        @click="editor.chain().focus().toggleBold().run()"
        :disabled="!editor.can().chain().focus().toggleBold().run()"
        :class="{ active: editor.isActive('bold') }"
        ><i class="ui icon bold"></i>
      </a>
      <a
        class="item"
        @click="editor.chain().focus().toggleItalic().run()"
        :disabled="!editor.can().chain().focus().toggleItalic().run()"
        :class="{ active: editor.isActive('italic') }"
        ><i class="ui icon italic"></i>
      </a>
      <a
        class="item"
        @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
        :class="{ active: editor.isActive('heading', { level: 1 }) }"
        ><i class="ui icon heading"></i>
      </a>

      <a
        class="item"
        @click="editor.chain().focus().toggleBulletList().run()"
        :class="{ active: editor.isActive('bulletList') }"
        ><i class="ui icon bullet list"></i>
      </a>
      <a
        class="item"
        @click="editor.chain().focus().toggleOrderedList().run()"
        :class="{ active: editor.isActive('orderedList') }"
        ><i class="ui icon ordered list"></i>
      </a>

      <a class="item" @click="editor.chain().focus().unsetAllMarks().run()"
        ><i class="ui icon remove format"></i>
      </a>
      <a
        class="item"
        @click="editor.chain().focus().undo().run()"
        :disabled="!editor.can().chain().focus().undo().run()"
        ><i class="ui icon undo"></i>
      </a>
      <a
        class="item"
        @click="editor.chain().focus().redo().run()"
        :disabled="!editor.can().chain().focus().redo().run()"
        ><i class="ui icon redo"></i>
      </a>
    </div>
    <div class="ui bottom attached segment" :class="{ loading }">
      <editor-content :editor="editor" />
    </div>
  </div>
</template>

<script>
import StarterKit from "@tiptap/starter-kit";
import { Editor, EditorContent, BubbleMenu, FloatingMenu } from "@tiptap/vue-3";
import Gpt from "./extensions/gpt";
import Commands from "./extensions/slash/commands";
import suggestion from "./extensions/slash/suggestion";

export default {
  components: {
    EditorContent,
    BubbleMenu,
    FloatingMenu,
  },

  props: {
    modelValue: {
      type: String,
      default: "",
    },
  },

  emits: ["update:modelValue"],

  data() {
    return {
      loading: false,
      editor: null,
    };
  },

  watch: {
    "editor.storage.gpt.loading": function (val) {
      this.loading = val;
    },
    modelValue(value) {
      // HTML
      const isSame = this.editor.getHTML() === value;

      // JSON
      // const isSame = JSON.stringify(this.editor.getJSON()) === JSON.stringify(value)

      if (isSame) {
        return;
      }

      this.editor.commands.setContent(value, false);
    },
  },

  methods: {},

  mounted() {
    this.editor = new Editor({
      autofocus: true,
      extensions: [
        StarterKit,
        Gpt,
        Commands.configure({
          suggestion,
        }),
      ],
      content: this.modelValue,
      onUpdate: () => {
        // HTML
        this.$emit("update:modelValue", this.editor.getHTML());

        // JSON
        // this.$emit('update:modelValue', this.editor.getJSON())
      },
    });
  },

  beforeUnmount() {
    this.editor.destroy();
  },
};
</script>

<style lang="scss">
.ui.menu {
  &.disabled {
    opacity: 0.8;
    .item {
      opacity: 0.2;
      pointer-events: none;
    }
  }
}

.ProseMirror:focus-visible {
  outline: none;
}

/* Basic editor styles */
.ProseMirror {
  > * + * {
    margin-top: 0.75em;
  }

  ul,
  ol {
    padding: 0 1rem;
  }

  blockquote {
    padding-left: 1rem;
    border-left: 2px solid rgba(#0d0d0d, 0.1);
  }
}

.bubble-menu {
  display: flex;
  background-color: #0d0d0d;
  padding: 0.2rem;
  border-radius: 0.5rem;

  button {
    border: none;
    background: none;
    color: #fff;
    font-size: 0.85rem;
    font-weight: 500;
    padding: 0 0.2rem;
    opacity: 0.6;

    &:hover,
    &.active {
      opacity: 1;
    }
  }
}

.floating-menu {
  display: flex;
  background-color: #0d0d0d10;
  padding: 0.2rem;
  border-radius: 0.5rem;

  button {
    border: none;
    background: none;
    font-size: 0.85rem;
    font-weight: 500;
    padding: 0 0.2rem;
    opacity: 0.6;

    &:hover,
    &.active {
      opacity: 1;
    }
  }
}
</style>
