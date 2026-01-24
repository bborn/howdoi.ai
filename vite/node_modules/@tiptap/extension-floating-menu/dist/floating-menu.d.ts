import { Extension } from '@tiptap/core';
import { FloatingMenuPluginProps } from './floating-menu-plugin.js';
export type FloatingMenuOptions = Omit<FloatingMenuPluginProps, 'editor' | 'element'> & {
    /**
     * The DOM element that contains your menu.
     * @type {HTMLElement}
     * @default null
     */
    element: HTMLElement | null;
};
/**
 * This extension allows you to create a floating menu.
 * @see https://tiptap.dev/api/extensions/floating-menu
 */
export declare const FloatingMenu: Extension<FloatingMenuOptions, any>;
//# sourceMappingURL=floating-menu.d.ts.map