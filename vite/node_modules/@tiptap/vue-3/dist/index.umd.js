(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports, require('@tiptap/extension-bubble-menu'), require('vue'), require('@tiptap/core'), require('@tiptap/extension-floating-menu')) :
  typeof define === 'function' && define.amd ? define(['exports', '@tiptap/extension-bubble-menu', 'vue', '@tiptap/core', '@tiptap/extension-floating-menu'], factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, factory(global["@tiptap/vue-3"] = {}, global.extensionBubbleMenu, global.vue, global.core, global.extensionFloatingMenu));
})(this, (function (exports, extensionBubbleMenu, vue, core, extensionFloatingMenu) { 'use strict';

  const BubbleMenu = vue.defineComponent({
      name: 'BubbleMenu',
      props: {
          pluginKey: {
              type: [String, Object],
              default: 'bubbleMenu',
          },
          editor: {
              type: Object,
              required: true,
          },
          updateDelay: {
              type: Number,
              default: undefined,
          },
          tippyOptions: {
              type: Object,
              default: () => ({}),
          },
          shouldShow: {
              type: Function,
              default: null,
          },
      },
      setup(props, { slots }) {
          const root = vue.ref(null);
          vue.onMounted(() => {
              const { updateDelay, editor, pluginKey, shouldShow, tippyOptions, } = props;
              editor.registerPlugin(extensionBubbleMenu.BubbleMenuPlugin({
                  updateDelay,
                  editor,
                  element: root.value,
                  pluginKey,
                  shouldShow,
                  tippyOptions,
              }));
          });
          vue.onBeforeUnmount(() => {
              const { pluginKey, editor } = props;
              editor.unregisterPlugin(pluginKey);
          });
          return () => { var _a; return vue.h('div', { ref: root }, (_a = slots.default) === null || _a === void 0 ? void 0 : _a.call(slots)); };
      },
  });

  /* eslint-disable react-hooks/rules-of-hooks */
  function useDebouncedRef(value) {
      return vue.customRef((track, trigger) => {
          return {
              get() {
                  track();
                  return value;
              },
              set(newValue) {
                  // update state
                  value = newValue;
                  // update view as soon as possible
                  requestAnimationFrame(() => {
                      requestAnimationFrame(() => {
                          trigger();
                      });
                  });
              },
          };
      });
  }
  class Editor extends core.Editor {
      constructor(options = {}) {
          super(options);
          this.contentComponent = null;
          this.appContext = null;
          this.reactiveState = useDebouncedRef(this.view.state);
          this.reactiveExtensionStorage = useDebouncedRef(this.extensionStorage);
          this.on('beforeTransaction', ({ nextState }) => {
              this.reactiveState.value = nextState;
              this.reactiveExtensionStorage.value = this.extensionStorage;
          });
          return vue.markRaw(this); // eslint-disable-line
      }
      get state() {
          return this.reactiveState ? this.reactiveState.value : this.view.state;
      }
      get storage() {
          return this.reactiveExtensionStorage ? this.reactiveExtensionStorage.value : super.storage;
      }
      /**
       * Register a ProseMirror plugin.
       */
      registerPlugin(plugin, handlePlugins) {
          const nextState = super.registerPlugin(plugin, handlePlugins);
          if (this.reactiveState) {
              this.reactiveState.value = nextState;
          }
          return nextState;
      }
      /**
       * Unregister a ProseMirror plugin.
       */
      unregisterPlugin(nameOrPluginKey) {
          const nextState = super.unregisterPlugin(nameOrPluginKey);
          if (this.reactiveState && nextState) {
              this.reactiveState.value = nextState;
          }
          return nextState;
      }
  }

  const EditorContent = vue.defineComponent({
      name: 'EditorContent',
      props: {
          editor: {
              default: null,
              type: Object,
          },
      },
      setup(props) {
          const rootEl = vue.ref();
          const instance = vue.getCurrentInstance();
          vue.watchEffect(() => {
              const editor = props.editor;
              if (editor && editor.options.element && rootEl.value) {
                  vue.nextTick(() => {
                      if (!rootEl.value || !editor.options.element.firstChild) {
                          return;
                      }
                      const element = vue.unref(rootEl.value);
                      rootEl.value.append(...editor.options.element.childNodes);
                      // @ts-ignore
                      editor.contentComponent = instance.ctx._;
                      if (instance) {
                          editor.appContext = {
                              ...instance.appContext,
                              // Vue internally uses prototype chain to forward/shadow injects across the entire component chain
                              // so don't use object spread operator or 'Object.assign' and just set `provides` as is on editor's appContext
                              // @ts-expect-error forward instance's 'provides' into appContext
                              provides: instance.provides,
                          };
                      }
                      editor.setOptions({
                          element,
                      });
                      editor.createNodeViews();
                  });
              }
          });
          vue.onBeforeUnmount(() => {
              const editor = props.editor;
              if (!editor) {
                  return;
              }
              editor.contentComponent = null;
              editor.appContext = null;
          });
          return { rootEl };
      },
      render() {
          return vue.h('div', {
              ref: (el) => { this.rootEl = el; },
          });
      },
  });

  const FloatingMenu = vue.defineComponent({
      name: 'FloatingMenu',
      props: {
          pluginKey: {
              // TODO: TypeScript breaks :(
              // type: [String, Object as PropType<Exclude<FloatingMenuPluginProps['pluginKey'], string>>],
              type: null,
              default: 'floatingMenu',
          },
          editor: {
              type: Object,
              required: true,
          },
          tippyOptions: {
              type: Object,
              default: () => ({}),
          },
          shouldShow: {
              type: Function,
              default: null,
          },
      },
      setup(props, { slots }) {
          const root = vue.ref(null);
          vue.onMounted(() => {
              const { pluginKey, editor, tippyOptions, shouldShow, } = props;
              editor.registerPlugin(extensionFloatingMenu.FloatingMenuPlugin({
                  pluginKey,
                  editor,
                  element: root.value,
                  tippyOptions,
                  shouldShow,
              }));
          });
          vue.onBeforeUnmount(() => {
              const { pluginKey, editor } = props;
              editor.unregisterPlugin(pluginKey);
          });
          return () => { var _a; return vue.h('div', { ref: root }, (_a = slots.default) === null || _a === void 0 ? void 0 : _a.call(slots)); };
      },
  });

  const NodeViewContent = vue.defineComponent({
      name: 'NodeViewContent',
      props: {
          as: {
              type: String,
              default: 'div',
          },
      },
      render() {
          return vue.h(this.as, {
              style: {
                  whiteSpace: 'pre-wrap',
              },
              'data-node-view-content': '',
          });
      },
  });

  const NodeViewWrapper = vue.defineComponent({
      name: 'NodeViewWrapper',
      props: {
          as: {
              type: String,
              default: 'div',
          },
      },
      inject: ['onDragStart', 'decorationClasses'],
      render() {
          var _a, _b;
          return vue.h(this.as, {
              // @ts-ignore
              class: this.decorationClasses,
              style: {
                  whiteSpace: 'normal',
              },
              'data-node-view-wrapper': '',
              // @ts-ignore (https://github.com/vuejs/vue-next/issues/3031)
              onDragstart: this.onDragStart,
          }, (_b = (_a = this.$slots).default) === null || _b === void 0 ? void 0 : _b.call(_a));
      },
  });

  const useEditor = (options = {}) => {
      const editor = vue.shallowRef();
      vue.onMounted(() => {
          editor.value = new Editor(options);
      });
      vue.onBeforeUnmount(() => {
          var _a, _b, _c;
          // Cloning root node (and its children) to avoid content being lost by destroy
          const nodes = (_a = editor.value) === null || _a === void 0 ? void 0 : _a.options.element;
          const newEl = nodes === null || nodes === void 0 ? void 0 : nodes.cloneNode(true);
          (_b = nodes === null || nodes === void 0 ? void 0 : nodes.parentNode) === null || _b === void 0 ? void 0 : _b.replaceChild(newEl, nodes);
          (_c = editor.value) === null || _c === void 0 ? void 0 : _c.destroy();
      });
      return editor;
  };

  /**
   * This class is used to render Vue components inside the editor.
   */
  class VueRenderer {
      constructor(component, { props = {}, editor }) {
          this.editor = editor;
          this.component = vue.markRaw(component);
          this.el = document.createElement('div');
          this.props = vue.reactive(props);
          this.renderedComponent = this.renderComponent();
      }
      get element() {
          return this.renderedComponent.el;
      }
      get ref() {
          var _a, _b, _c, _d;
          // Composition API
          if ((_b = (_a = this.renderedComponent.vNode) === null || _a === void 0 ? void 0 : _a.component) === null || _b === void 0 ? void 0 : _b.exposed) {
              return this.renderedComponent.vNode.component.exposed;
          }
          // Option API
          return (_d = (_c = this.renderedComponent.vNode) === null || _c === void 0 ? void 0 : _c.component) === null || _d === void 0 ? void 0 : _d.proxy;
      }
      renderComponent() {
          let vNode = vue.h(this.component, this.props);
          if (this.editor.appContext) {
              vNode.appContext = this.editor.appContext;
          }
          if (typeof document !== 'undefined' && this.el) {
              vue.render(vNode, this.el);
          }
          const destroy = () => {
              if (this.el) {
                  vue.render(null, this.el);
              }
              this.el = null;
              vNode = null;
          };
          return { vNode, destroy, el: this.el ? this.el.firstElementChild : null };
      }
      updateProps(props = {}) {
          Object.entries(props).forEach(([key, value]) => {
              this.props[key] = value;
          });
          this.renderComponent();
      }
      destroy() {
          this.renderedComponent.destroy();
      }
  }

  /* eslint-disable no-underscore-dangle */
  const nodeViewProps = {
      editor: {
          type: Object,
          required: true,
      },
      node: {
          type: Object,
          required: true,
      },
      decorations: {
          type: Object,
          required: true,
      },
      selected: {
          type: Boolean,
          required: true,
      },
      extension: {
          type: Object,
          required: true,
      },
      getPos: {
          type: Function,
          required: true,
      },
      updateAttributes: {
          type: Function,
          required: true,
      },
      deleteNode: {
          type: Function,
          required: true,
      },
      view: {
          type: Object,
          required: true,
      },
      innerDecorations: {
          type: Object,
          required: true,
      },
      HTMLAttributes: {
          type: Object,
          required: true,
      },
  };
  class VueNodeView extends core.NodeView {
      mount() {
          const props = {
              editor: this.editor,
              node: this.node,
              decorations: this.decorations,
              innerDecorations: this.innerDecorations,
              view: this.view,
              selected: false,
              extension: this.extension,
              HTMLAttributes: this.HTMLAttributes,
              getPos: () => this.getPos(),
              updateAttributes: (attributes = {}) => this.updateAttributes(attributes),
              deleteNode: () => this.deleteNode(),
          };
          const onDragStart = this.onDragStart.bind(this);
          this.decorationClasses = vue.ref(this.getDecorationClasses());
          const extendedComponent = vue.defineComponent({
              extends: { ...this.component },
              props: Object.keys(props),
              template: this.component.template,
              setup: reactiveProps => {
                  var _a, _b;
                  vue.provide('onDragStart', onDragStart);
                  vue.provide('decorationClasses', this.decorationClasses);
                  return (_b = (_a = this.component).setup) === null || _b === void 0 ? void 0 : _b.call(_a, reactiveProps, {
                      expose: () => undefined,
                  });
              },
              // add support for scoped styles
              // @ts-ignore
              // eslint-disable-next-line
              __scopeId: this.component.__scopeId,
              // add support for CSS Modules
              // @ts-ignore
              // eslint-disable-next-line
              __cssModules: this.component.__cssModules,
              // add support for vue devtools
              // @ts-ignore
              // eslint-disable-next-line
              __name: this.component.__name,
              // @ts-ignore
              // eslint-disable-next-line
              __file: this.component.__file,
          });
          this.handleSelectionUpdate = this.handleSelectionUpdate.bind(this);
          this.editor.on('selectionUpdate', this.handleSelectionUpdate);
          this.renderer = new VueRenderer(extendedComponent, {
              editor: this.editor,
              props,
          });
      }
      /**
       * Return the DOM element.
       * This is the element that will be used to display the node view.
       */
      get dom() {
          if (!this.renderer.element || !this.renderer.element.hasAttribute('data-node-view-wrapper')) {
              throw Error('Please use the NodeViewWrapper component for your node view.');
          }
          return this.renderer.element;
      }
      /**
       * Return the content DOM element.
       * This is the element that will be used to display the rich-text content of the node.
       */
      get contentDOM() {
          if (this.node.isLeaf) {
              return null;
          }
          return this.dom.querySelector('[data-node-view-content]');
      }
      /**
       * On editor selection update, check if the node is selected.
       * If it is, call `selectNode`, otherwise call `deselectNode`.
       */
      handleSelectionUpdate() {
          const { from, to } = this.editor.state.selection;
          const pos = this.getPos();
          if (typeof pos !== 'number') {
              return;
          }
          if (from <= pos && to >= pos + this.node.nodeSize) {
              if (this.renderer.props.selected) {
                  return;
              }
              this.selectNode();
          }
          else {
              if (!this.renderer.props.selected) {
                  return;
              }
              this.deselectNode();
          }
      }
      /**
       * On update, update the React component.
       * To prevent unnecessary updates, the `update` option can be used.
       */
      update(node, decorations, innerDecorations) {
          const rerenderComponent = (props) => {
              this.decorationClasses.value = this.getDecorationClasses();
              this.renderer.updateProps(props);
          };
          if (typeof this.options.update === 'function') {
              const oldNode = this.node;
              const oldDecorations = this.decorations;
              const oldInnerDecorations = this.innerDecorations;
              this.node = node;
              this.decorations = decorations;
              this.innerDecorations = innerDecorations;
              return this.options.update({
                  oldNode,
                  oldDecorations,
                  newNode: node,
                  newDecorations: decorations,
                  oldInnerDecorations,
                  innerDecorations,
                  updateProps: () => rerenderComponent({ node, decorations, innerDecorations }),
              });
          }
          if (node.type !== this.node.type) {
              return false;
          }
          if (node === this.node && this.decorations === decorations && this.innerDecorations === innerDecorations) {
              return true;
          }
          this.node = node;
          this.decorations = decorations;
          this.innerDecorations = innerDecorations;
          rerenderComponent({ node, decorations, innerDecorations });
          return true;
      }
      /**
       * Select the node.
       * Add the `selected` prop and the `ProseMirror-selectednode` class.
       */
      selectNode() {
          this.renderer.updateProps({
              selected: true,
          });
          if (this.renderer.element) {
              this.renderer.element.classList.add('ProseMirror-selectednode');
          }
      }
      /**
       * Deselect the node.
       * Remove the `selected` prop and the `ProseMirror-selectednode` class.
       */
      deselectNode() {
          this.renderer.updateProps({
              selected: false,
          });
          if (this.renderer.element) {
              this.renderer.element.classList.remove('ProseMirror-selectednode');
          }
      }
      getDecorationClasses() {
          return (this.decorations
              // @ts-ignore
              .map(item => item.type.attrs.class)
              .flat()
              .join(' '));
      }
      destroy() {
          this.renderer.destroy();
          this.editor.off('selectionUpdate', this.handleSelectionUpdate);
      }
  }
  function VueNodeViewRenderer(component, options) {
      return props => {
          // try to get the parent component
          // this is important for vue devtools to show the component hierarchy correctly
          // maybe it’s `undefined` because <editor-content> isn’t rendered yet
          if (!props.editor.contentComponent) {
              return {};
          }
          // check for class-component and normalize if neccessary
          const normalizedComponent = typeof component === 'function' && '__vccOpts' in component
              ? component.__vccOpts
              : component;
          return new VueNodeView(normalizedComponent, props, options);
      };
  }

  exports.BubbleMenu = BubbleMenu;
  exports.Editor = Editor;
  exports.EditorContent = EditorContent;
  exports.FloatingMenu = FloatingMenu;
  exports.NodeViewContent = NodeViewContent;
  exports.NodeViewWrapper = NodeViewWrapper;
  exports.VueNodeViewRenderer = VueNodeViewRenderer;
  exports.VueRenderer = VueRenderer;
  exports.nodeViewProps = nodeViewProps;
  exports.useEditor = useEditor;
  Object.keys(core).forEach(function (k) {
    if (k !== 'default' && !Object.prototype.hasOwnProperty.call(exports, k)) Object.defineProperty(exports, k, {
      enumerable: true,
      get: function () { return core[k]; }
    });
  });

}));
//# sourceMappingURL=index.umd.js.map
