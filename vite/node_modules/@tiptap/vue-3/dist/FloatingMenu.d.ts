import { FloatingMenuPluginProps } from '@tiptap/extension-floating-menu';
import { PropType } from 'vue';
export declare const FloatingMenu: import("vue").DefineComponent<import("vue").ExtractPropTypes<{
    pluginKey: {
        type: null;
        default: string;
    };
    editor: {
        type: PropType<FloatingMenuPluginProps["editor"]>;
        required: true;
    };
    tippyOptions: {
        type: PropType<FloatingMenuPluginProps["tippyOptions"]>;
        default: () => {};
    };
    shouldShow: {
        type: PropType<Exclude<Required<FloatingMenuPluginProps>["shouldShow"], null>>;
        default: null;
    };
}>, () => import("vue").VNode<import("vue").RendererNode, import("vue").RendererElement, {
    [key: string]: any;
}>, {}, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    pluginKey: {
        type: null;
        default: string;
    };
    editor: {
        type: PropType<FloatingMenuPluginProps["editor"]>;
        required: true;
    };
    tippyOptions: {
        type: PropType<FloatingMenuPluginProps["tippyOptions"]>;
        default: () => {};
    };
    shouldShow: {
        type: PropType<Exclude<Required<FloatingMenuPluginProps>["shouldShow"], null>>;
        default: null;
    };
}>> & Readonly<{}>, {
    tippyOptions: Partial<import("tippy.js").Props> | undefined;
    shouldShow: (props: {
        editor: import("@tiptap/core").Editor;
        view: import("prosemirror-view").EditorView;
        state: import("prosemirror-state").EditorState;
        oldState?: import("prosemirror-state").EditorState;
    }) => boolean;
    pluginKey: any;
}, {}, {}, {}, string, import("vue").ComponentProvideOptions, true, {}, any>;
//# sourceMappingURL=FloatingMenu.d.ts.map