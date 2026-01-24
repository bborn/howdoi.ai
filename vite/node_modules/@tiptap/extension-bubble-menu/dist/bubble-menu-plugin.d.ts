import { Editor } from '@tiptap/core';
import { EditorState, Plugin, PluginKey } from '@tiptap/pm/state';
import { EditorView } from '@tiptap/pm/view';
import { Instance, Props } from 'tippy.js';
export interface BubbleMenuPluginProps {
    /**
     * The plugin key.
     * @type {PluginKey | string}
     * @default 'bubbleMenu'
     */
    pluginKey: PluginKey | string;
    /**
     * The editor instance.
     */
    editor: Editor;
    /**
     * The DOM element that contains your menu.
     * @type {HTMLElement}
     * @default null
     */
    element: HTMLElement;
    /**
     * The options for the tippy.js instance.
     * @see https://atomiks.github.io/tippyjs/v6/all-props/
     */
    tippyOptions?: Partial<Props>;
    /**
     * The delay in milliseconds before the menu should be updated.
     * This can be useful to prevent performance issues.
     * @type {number}
     * @default 250
     */
    updateDelay?: number;
    /**
     * A function that determines whether the menu should be shown or not.
     * If this function returns `false`, the menu will be hidden, otherwise it will be shown.
     */
    shouldShow?: ((props: {
        editor: Editor;
        element: HTMLElement;
        view: EditorView;
        state: EditorState;
        oldState?: EditorState;
        from: number;
        to: number;
    }) => boolean) | null;
}
export type BubbleMenuViewProps = BubbleMenuPluginProps & {
    view: EditorView;
};
export declare class BubbleMenuView {
    editor: Editor;
    element: HTMLElement;
    view: EditorView;
    preventHide: boolean;
    tippy: Instance | undefined;
    tippyOptions?: Partial<Props>;
    updateDelay: number;
    private updateDebounceTimer;
    shouldShow: Exclude<BubbleMenuPluginProps['shouldShow'], null>;
    constructor({ editor, element, view, tippyOptions, updateDelay, shouldShow, }: BubbleMenuViewProps);
    mousedownHandler: () => void;
    dragstartHandler: () => void;
    focusHandler: () => void;
    blurHandler: ({ event }: {
        event: FocusEvent;
    }) => void;
    tippyBlurHandler: (event: FocusEvent) => void;
    createTooltip(): void;
    update(view: EditorView, oldState?: EditorState): void;
    handleDebouncedUpdate: (view: EditorView, oldState?: EditorState) => void;
    updateHandler: (view: EditorView, selectionChanged: boolean, docChanged: boolean, oldState?: EditorState) => void;
    show(): void;
    hide(): void;
    destroy(): void;
}
export declare const BubbleMenuPlugin: (options: BubbleMenuPluginProps) => Plugin<any>;
//# sourceMappingURL=bubble-menu-plugin.d.ts.map