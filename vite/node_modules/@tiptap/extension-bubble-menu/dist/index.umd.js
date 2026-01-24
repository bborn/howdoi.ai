(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports, require('@tiptap/core'), require('@tiptap/pm/state'), require('tippy.js')) :
  typeof define === 'function' && define.amd ? define(['exports', '@tiptap/core', '@tiptap/pm/state', 'tippy.js'], factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, factory(global["@tiptap/extension-bubble-menu"] = {}, global.core, global.state, global.tippy));
})(this, (function (exports, core, state, tippy) { 'use strict';

  class BubbleMenuView {
      constructor({ editor, element, view, tippyOptions = {}, updateDelay = 250, shouldShow, }) {
          this.preventHide = false;
          this.shouldShow = ({ view, state, from, to, }) => {
              const { doc, selection } = state;
              const { empty } = selection;
              // Sometime check for `empty` is not enough.
              // Doubleclick an empty paragraph returns a node size of 2.
              // So we check also for an empty text size.
              const isEmptyTextBlock = !doc.textBetween(from, to).length && core.isTextSelection(state.selection);
              // When clicking on a element inside the bubble menu the editor "blur" event
              // is called and the bubble menu item is focussed. In this case we should
              // consider the menu as part of the editor and keep showing the menu
              const isChildOfMenu = this.element.contains(document.activeElement);
              const hasEditorFocus = view.hasFocus() || isChildOfMenu;
              if (!hasEditorFocus || empty || isEmptyTextBlock || !this.editor.isEditable) {
                  return false;
              }
              return true;
          };
          this.mousedownHandler = () => {
              this.preventHide = true;
          };
          this.dragstartHandler = () => {
              this.hide();
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
          this.handleDebouncedUpdate = (view, oldState) => {
              const selectionChanged = !(oldState === null || oldState === void 0 ? void 0 : oldState.selection.eq(view.state.selection));
              const docChanged = !(oldState === null || oldState === void 0 ? void 0 : oldState.doc.eq(view.state.doc));
              if (!selectionChanged && !docChanged) {
                  return;
              }
              if (this.updateDebounceTimer) {
                  clearTimeout(this.updateDebounceTimer);
              }
              this.updateDebounceTimer = window.setTimeout(() => {
                  this.updateHandler(view, selectionChanged, docChanged, oldState);
              }, this.updateDelay);
          };
          this.updateHandler = (view, selectionChanged, docChanged, oldState) => {
              var _a, _b, _c;
              const { state, composing } = view;
              const { selection } = state;
              const isSame = !selectionChanged && !docChanged;
              if (composing || isSame) {
                  return;
              }
              this.createTooltip();
              // support for CellSelections
              const { ranges } = selection;
              const from = Math.min(...ranges.map(range => range.$from.pos));
              const to = Math.max(...ranges.map(range => range.$to.pos));
              const shouldShow = (_a = this.shouldShow) === null || _a === void 0 ? void 0 : _a.call(this, {
                  editor: this.editor,
                  element: this.element,
                  view,
                  state,
                  oldState,
                  from,
                  to,
              });
              if (!shouldShow) {
                  this.hide();
                  return;
              }
              (_b = this.tippy) === null || _b === void 0 ? void 0 : _b.setProps({
                  getReferenceClientRect: ((_c = this.tippyOptions) === null || _c === void 0 ? void 0 : _c.getReferenceClientRect)
                      || (() => {
                          if (core.isNodeSelection(state.selection)) {
                              let node = view.nodeDOM(from);
                              if (node) {
                                  const nodeViewWrapper = node.dataset.nodeViewWrapper ? node : node.querySelector('[data-node-view-wrapper]');
                                  if (nodeViewWrapper) {
                                      node = nodeViewWrapper.firstChild;
                                  }
                                  if (node) {
                                      return node.getBoundingClientRect();
                                  }
                              }
                          }
                          return core.posToDOMRect(view, from, to);
                      }),
              });
              this.show();
          };
          this.editor = editor;
          this.element = element;
          this.view = view;
          this.updateDelay = updateDelay;
          if (shouldShow) {
              this.shouldShow = shouldShow;
          }
          this.element.addEventListener('mousedown', this.mousedownHandler, { capture: true });
          this.view.dom.addEventListener('dragstart', this.dragstartHandler);
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
              placement: 'top',
              hideOnClick: 'toggle',
              ...this.tippyOptions,
          });
          // maybe we have to hide tippy on its own blur event as well
          if (this.tippy.popper.firstChild) {
              this.tippy.popper.firstChild.addEventListener('blur', this.tippyBlurHandler);
          }
      }
      update(view, oldState) {
          const { state } = view;
          const hasValidSelection = state.selection.from !== state.selection.to;
          if (this.updateDelay > 0 && hasValidSelection) {
              this.handleDebouncedUpdate(view, oldState);
              return;
          }
          const selectionChanged = !(oldState === null || oldState === void 0 ? void 0 : oldState.selection.eq(view.state.selection));
          const docChanged = !(oldState === null || oldState === void 0 ? void 0 : oldState.doc.eq(view.state.doc));
          this.updateHandler(view, selectionChanged, docChanged, oldState);
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
          this.view.dom.removeEventListener('dragstart', this.dragstartHandler);
          this.editor.off('focus', this.focusHandler);
          this.editor.off('blur', this.blurHandler);
      }
  }
  const BubbleMenuPlugin = (options) => {
      return new state.Plugin({
          key: typeof options.pluginKey === 'string' ? new state.PluginKey(options.pluginKey) : options.pluginKey,
          view: view => new BubbleMenuView({ view, ...options }),
      });
  };

  /**
   * This extension allows you to create a bubble menu.
   * @see https://tiptap.dev/api/extensions/bubble-menu
   */
  const BubbleMenu = core.Extension.create({
      name: 'bubbleMenu',
      addOptions() {
          return {
              element: null,
              tippyOptions: {},
              pluginKey: 'bubbleMenu',
              updateDelay: undefined,
              shouldShow: null,
          };
      },
      addProseMirrorPlugins() {
          if (!this.options.element) {
              return [];
          }
          return [
              BubbleMenuPlugin({
                  pluginKey: this.options.pluginKey,
                  editor: this.editor,
                  element: this.options.element,
                  tippyOptions: this.options.tippyOptions,
                  updateDelay: this.options.updateDelay,
                  shouldShow: this.options.shouldShow,
              }),
          ];
      },
  });

  exports.BubbleMenu = BubbleMenu;
  exports.BubbleMenuPlugin = BubbleMenuPlugin;
  exports.BubbleMenuView = BubbleMenuView;
  exports.default = BubbleMenu;

  Object.defineProperty(exports, '__esModule', { value: true });

}));
//# sourceMappingURL=index.umd.js.map
