import { BubbleMenuPluginProps } from '@tiptap/extension-bubble-menu';
import { PropType } from 'vue';
export declare const BubbleMenu: import("vue").DefineComponent<import("vue").ExtractPropTypes<{
    pluginKey: {
        type: PropType<BubbleMenuPluginProps["pluginKey"]>;
        default: string;
    };
    editor: {
        type: PropType<BubbleMenuPluginProps["editor"]>;
        required: true;
    };
    updateDelay: {
        type: PropType<BubbleMenuPluginProps["updateDelay"]>;
        default: undefined;
    };
    tippyOptions: {
        type: PropType<BubbleMenuPluginProps["tippyOptions"]>;
        default: () => {};
    };
    shouldShow: {
        type: PropType<Exclude<Required<BubbleMenuPluginProps>["shouldShow"], null>>;
        default: null;
    };
}>, () => import("vue").VNode<import("vue").RendererNode, import("vue").RendererElement, {
    [key: string]: any;
}>, {}, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    pluginKey: {
        type: PropType<BubbleMenuPluginProps["pluginKey"]>;
        default: string;
    };
    editor: {
        type: PropType<BubbleMenuPluginProps["editor"]>;
        required: true;
    };
    updateDelay: {
        type: PropType<BubbleMenuPluginProps["updateDelay"]>;
        default: undefined;
    };
    tippyOptions: {
        type: PropType<BubbleMenuPluginProps["tippyOptions"]>;
        default: () => {};
    };
    shouldShow: {
        type: PropType<Exclude<Required<BubbleMenuPluginProps>["shouldShow"], null>>;
        default: null;
    };
}>> & Readonly<{}>, {
    pluginKey: string | import("prosemirror-state").PluginKey<any>;
    updateDelay: number | undefined;
    tippyOptions: Partial<import("tippy.js").Props> | undefined;
    shouldShow: (props: {
        editor: import("@tiptap/core").Editor;
        element: HTMLElement;
        view: import("prosemirror-view").EditorView;
        state: import("prosemirror-state").EditorState;
        oldState?: import("prosemirror-state").EditorState;
        from: number;
        to: number;
    }) => boolean;
}, {}, {}, {}, string, import("vue").ComponentProvideOptions, true, {}, any>;
//# sourceMappingURL=BubbleMenu.d.ts.map