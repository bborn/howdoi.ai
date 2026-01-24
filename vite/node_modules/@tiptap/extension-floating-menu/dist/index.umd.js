(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports, require('@tiptap/core'), require('@tiptap/pm/state'), require('tippy.js')) :
  typeof define === 'function' && define.amd ? define(['exports', '@tiptap/core', '@tiptap/pm/state', 'tippy.js'], factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, factory(global["@tiptap/extension-floating-menu"] = {}, global.core, global.state, global.tippy));
})(this, (function (exports, core, state, tippy) { 'use strict';

  class FloatingMenuView {
      getTextContent(node) {
          return core.getText(node, { textSerializers: core.getTextSerializersFromSchema(this.editor.schema) });
      }
      constructor({ editor, element, view, tippyOptions = {}, shouldShow, }) {
          this.preventHide = false;
          this.shouldShow = ({ view, state }) => {
              const { selection } = state;
              const { $anchor, empty } = selection;
              const isRootDepth = $anchor.depth === 1;
              const isEmptyTextBlock = $anchor.parent.isTextblock && !$anchor.parent.type.spec.code && !$anchor.parent.textContent && $anchor.parent.childCount === 0 && !this.getTextContent($anchor.parent);
              if (!view.hasFocus()
                  || !empty
                  || !isRootDepth
                  || !isEmptyTextBlock
                  || !this.editor.isEditable) {
                  return false;
              }
              return true;
          };
          this.mousedownHandler = () => {
              this.preventHide = true;
          };
          this.focusHandler = () => {
              // we use `setTimeout` to make sure `selection` is already updated
              setTimeout(() => this.update(this.editor.view));
          };
          this.blurHandler = ({ event }) => {
              var _a;
              if (this.preventHide) {
                  this.preventHide = false;
                  return;
              }
              if ((event === null || event === void 0 ? void 0 : event.relatedTarget) && ((_a = this.element.parentNode) === null || _a === void 0 ? void 0 : _a.contains(event.relatedTarget))) {
                  return;
              }
              if ((event === null || event === void 0 ? void 0 : event.relatedTarget) === this.editor.view.dom) {
                  return;
              }
              this.hide();
          };
          this.tippyBlurHandler = (event) => {
              this.blurHandler({ event });
          };
          this.editor = editor;
          this.element = element;
          this.view = view;
          if (shouldShow) {
              this.shouldShow = shouldShow;
          }
          this.element.addEventListener('mousedown', this.mousedownHandler, { capture: true });
          this.editor.on('focus', this.focusHandler);
          this.editor.on('blur', this.blurHandler);
          this.tippyOptions = tippyOptions;
          // Detaches menu content from its current parent
          this.element.remove();
          this.element.style.visibility = 'visible';
      }
      createTooltip() {
          const { element: editorElement } = this.editor.options;
          const editorIsAttached = !!editorElement.parentElement;
          this.element.tabIndex = 0;
          if (this.tippy || !editorIsAttached) {
              return;
          }
          this.tippy = tippy(editorElement, {
              duration: 0,
              getReferenceClientRect: null,
              content: this.element,
              interactive: true,
              trigger: 'manual',
              placement: 'right',
              hideOnClick: 'toggle',
              ...this.tippyOptions,
          });
          // maybe we have to hide tippy on its own blur event as well
          if (this.tippy.popper.firstChild) {
              this.tippy.popper.firstChild.addEventListener('blur', this.tippyBlurHandler);
          }
      }
      update(view, oldState) {
          var _a, _b, _c;
          const { state } = view;
          const { doc, selection } = state;
          const { from, to } = selection;
          const isSame = oldState && oldState.doc.eq(doc) && oldState.selection.eq(selection);
          if (isSame) {
              return;
          }
          this.createTooltip();
          const shouldShow = (_a = this.shouldShow) === null || _a === void 0 ? void 0 : _a.call(this, {
              editor: this.editor,
              view,
              state,
              oldState,
          });
          if (!shouldShow) {
              this.hide();
              return;
          }
          (_b = this.tippy) === null || _b === void 0 ? void 0 : _b.setProps({
              getReferenceClientRect: ((_c = this.tippyOptions) === null || _c === void 0 ? void 0 : _c.getReferenceClientRect) || (() => core.posToDOMRect(view, from, to)),
          });
          this.show();
      }
      show() {
          var _a;
          (_a = this.tippy) === null || _a === void 0 ? void 0 : _a.show();
      }
      hide() {
          var _a;
          (_a = this.tippy) === null || _a === void 0 ? void 0 : _a.hide();
      }
      destroy() {
          var _a, _b;
          if ((_a = this.tippy) === null || _a === void 0 ? void 0 : _a.popper.firstChild) {
              this.tippy.popper.firstChild.removeEventListener('blur', this.tippyBlurHandler);
          }
          (_b = this.tippy) === null || _b === void 0 ? void 0 : _b.destroy();
          this.element.removeEventListener('mousedown', this.mousedownHandler, { capture: true });
          this.editor.off('focus', this.focusHandler);
          this.editor.off('blur', this.blurHandler);
      }
  }
  const FloatingMenuPlugin = (options) => {
      return new state.Plugin({
          key: typeof options.pluginKey === 'string' ? new state.PluginKey(options.pluginKey) : options.pluginKey,
          view: view => new FloatingMenuView({ view, ...options }),
      });
  };

  /**
   * This extension allows you to create a floating menu.
   * @see https://tiptap.dev/api/extensions/floating-menu
   */
  const FloatingMenu = core.Extension.create({
      name: 'floatingMenu',
      addOptions() {
          return {
              element: null,
              tippyOptions: {},
              pluginKey: 'floatingMenu',
              shouldShow: null,
          };
      },
      addProseMirrorPlugins() {
          if (!this.options.element) {
              return [];
          }
          return [
              FloatingMenuPlugin({
                  pluginKey: this.options.pluginKey,
                  editor: this.editor,
                  element: this.options.element,
                  tippyOptions: this.options.tippyOptions,
                  shouldShow: this.options.shouldShow,
              }),
          ];
      },
  });

  exports.FloatingMenu = FloatingMenu;
  exports.FloatingMenuPlugin = FloatingMenuPlugin;
  exports.FloatingMenuView = FloatingMenuView;
  exports.default = FloatingMenu;

  Object.defineProperty(exports, '__esModule', { value: true });

}));
//# sourceMappingURL=index.umd.js.map
