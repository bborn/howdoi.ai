import { nextTick, withDirectives, openBlock, createElementBlock, normalizeStyle, vModelText } from "vue";
var _export_sfc = (sfc, props) => {
  const target = sfc.__vccOpts || sfc;
  for (const [key, val] of props) {
    target[key] = val;
  }
  return target;
};
const _sfc_main = {
  name: "ResizeTextarea",
  props: {
    placeholder: {
      type: String,
      default: ""
    },
    rows: {
      type: Number,
      default: 2
    },
    cols: {
      type: Number,
      default: 0
    },
    minHeight: {
      type: Number,
      default: 50
    },
    maxHeight: {
      type: Number,
      default: null
    },
    modelValue: {
      type: [String, Number],
      default: ""
    },
    autoResize: {
      type: Boolean,
      default: true
    }
  },
  emits: ["update:modelValue"],
  data() {
    return {
      textareaContent: "",
      height: "",
      isScrollEnabled: false
    };
  },
  computed: {
    styles() {
      return {
        resize: this.autoResize ? "none !important" : "",
        padding: `5${this.unit}`,
        height: this.height,
        overflow: `${this.isScrollEnabled ? "scroll" : "hidden"} !important`
      };
    },
    unit() {
      return "px";
    }
  },
  watch: {
    textareaContent() {
      this.$emit("update:modelValue", this.textareaContent);
      this.resize();
    }
  },
  methods: {
    resize() {
      const element = this.$refs.textarea;
      this.height = "auto !important";
      nextTick(() => {
        if (this.minHeight) {
          this.height = `${element.scrollHeight < this.minHeight ? this.minHeight : element.scrollHeight}${this.unit}`;
        }
        if (this.maxHeight) {
          if (element.scrollHeight > this.maxHeight) {
            this.height = `${this.maxHeight}${this.unit}`;
            this.isScrollEnabled = true;
          } else {
            this.isScrollEnabled = false;
          }
        }
      });
    }
  },
  created() {
    nextTick(() => {
      this.textareaContent = this.modelValue;
    });
  },
  mounted() {
    this.resize();
  }
};
const _hoisted_1 = ["rows", "cols", "placeholder"];
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return withDirectives((openBlock(), createElementBlock("textarea", {
    style: normalizeStyle($options.styles),
    ref: "textarea",
    rows: $props.rows,
    cols: $props.cols,
    placeholder: $props.placeholder,
    wrap: "hard",
    onFocus: _cache[0] || (_cache[0] = (...args) => $options.resize && $options.resize(...args)),
    "onUpdate:modelValue": _cache[1] || (_cache[1] = ($event) => $data.textareaContent = $event)
  }, null, 44, _hoisted_1)), [
    [vModelText, $data.textareaContent]
  ]);
}
var ResizeTextarea = /* @__PURE__ */ _export_sfc(_sfc_main, [["render", _sfc_render]]);
var index = {
  install: (app, options) => {
    app.component("resize-textarea", ResizeTextarea);
  }
};
export { index as default };
