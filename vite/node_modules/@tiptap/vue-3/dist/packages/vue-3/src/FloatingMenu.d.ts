import { PropType } from 'vue';
export declare const FloatingMenu: import("vue").DefineComponent<{
    pluginKey: {
        type: null;
        default: string;
    };
    editor: {
        type: PropType<import("@tiptap/core").Editor>;
        required: true;
    };
    tippyOptions: {
        type: PropType<Partial<import("tippy.js").Props> | undefined>;
        default: () => {};
    };
    shouldShow: {
        type: PropType<(props: {
            editor: import("@tiptap/core").Editor;
            view: import("prosemirror-view").EditorView;
            state: import("prosemirror-state").EditorState;
            oldState?: import("prosemirror-state").EditorState | undefined;
        }) => boolean>;
        default: null;
    };
}, () => import("vue").VNode<import("vue").RendererNode, import("vue").RendererElement, {
    [key: string]: any;
}>, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, Record<string, any>, string, import("vue").VNodeProps & import("vue").AllowedComponentProps & import("vue").ComponentCustomProps, Readonly<import("vue").ExtractPropTypes<{
    pluginKey: {
        type: null;
        default: string;
    };
    editor: {
        type: PropType<import("@tiptap/core").Editor>;
        required: true;
    };
    tippyOptions: {
        type: PropType<Partial<import("tippy.js").Props> | undefined>;
        default: () => {};
    };
    shouldShow: {
        type: PropType<(props: {
            editor: import("@tiptap/core").Editor;
            view: import("prosemirror-view").EditorView;
            state: import("prosemirror-state").EditorState;
            oldState?: import("prosemirror-state").EditorState | undefined;
        }) => boolean>;
        default: null;
    };
}>>, {
    tippyOptions: Partial<import("tippy.js").Props> | undefined;
    shouldShow: (props: {
        editor: import("@tiptap/core").Editor;
        view: import("prosemirror-view").EditorView;
        state: import("prosemirror-state").EditorState;
        oldState?: import("prosemirror-state").EditorState | undefined;
    }) => boolean;
    pluginKey: any;
}>;
