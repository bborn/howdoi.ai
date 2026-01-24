import { Editor } from '@tiptap/core';
import { EditorState, Plugin, PluginKey } from '@tiptap/pm/state';
import { EditorView } from '@tiptap/pm/view';
import { Instance, Props } from 'tippy.js';
export interface FloatingMenuPluginProps {
    /**
     * The plugin key for the floating menu.
     * @default 'floatingMenu'
     */
    pluginKey: PluginKey | string;
    /**
     * The editor instance.
     * @default null
     */
    editor: Editor;
    /**
     * The DOM element that contains your menu.
     * @default null
     */
    element: HTMLElement;
    /**
     * The options for the tippy instance.
     * @default {}
     * @see https://atomiks.github.io/tippyjs/v6/all-props/
     */
    tippyOptions?: Partial<Props>;
    /**
     * A function that determines whether the menu should be shown or not.
     * If this function returns `false`, the menu will be hidden, otherwise it will be shown.
     * @default null
     */
    shouldShow?: ((props: {
        editor: Editor;
        view: EditorView;
        state: EditorState;
        oldState?: EditorState;
    }) => boolean) | null;
}
export type FloatingMenuViewProps = FloatingMenuPluginProps & {
    /**
     * The editor view.
     */
    view: EditorView;
};
export declare class FloatingMenuView {
    editor: Editor;
    element: HTMLElement;
    view: EditorView;
    preventHide: boolean;
    tippy: Instance | undefined;
    tippyOptions?: Partial<Props>;
    private getTextContent;
    shouldShow: Exclude<FloatingMenuPluginProps['shouldShow'], null>;
    constructor({ editor, element, view, tippyOptions, shouldShow, }: FloatingMenuViewProps);
    mousedownHandler: () => void;
    focusHandler: () => void;
    blurHandler: ({ event }: {
        event: FocusEvent;
    }) => void;
    tippyBlurHandler: (event: FocusEvent) => void;
    createTooltip(): void;
    update(view: EditorView, oldState?: EditorState): void;
    show(): void;
    hide(): void;
    destroy(): void;
}
export declare const FloatingMenuPlugin: (options: FloatingMenuPluginProps) => Plugin<any>;
//# sourceMappingURL=floating-menu-plugin.d.ts.map