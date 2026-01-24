import { Extension } from '@tiptap/core';
import { BubbleMenuPluginProps } from './bubble-menu-plugin.js';
export type BubbleMenuOptions = Omit<BubbleMenuPluginProps, 'editor' | 'element'> & {
    /**
     * The DOM element that contains your menu.
     * @type {HTMLElement}
     * @default null
     */
    element: HTMLElement | null;
};
/**
 * This extension allows you to create a bubble menu.
 * @see https://tiptap.dev/api/extensions/bubble-menu
 */
export declare const BubbleMenu: Extension<BubbleMenuOptions, any>;
//# sourceMappingURL=bubble-menu.d.ts.map