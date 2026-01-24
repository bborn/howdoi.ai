import { NodeViewProps, NodeViewRenderer, NodeViewRendererOptions } from '@tiptap/core';
import { Node as ProseMirrorNode } from '@tiptap/pm/model';
import { Decoration, DecorationSource } from '@tiptap/pm/view';
import { Component, PropType } from 'vue';
export declare const nodeViewProps: {
    editor: {
        type: PropType<NodeViewProps["editor"]>;
        required: true;
    };
    node: {
        type: PropType<NodeViewProps["node"]>;
        required: true;
    };
    decorations: {
        type: PropType<NodeViewProps["decorations"]>;
        required: true;
    };
    selected: {
        type: PropType<NodeViewProps["selected"]>;
        required: true;
    };
    extension: {
        type: PropType<NodeViewProps["extension"]>;
        required: true;
    };
    getPos: {
        type: PropType<NodeViewProps["getPos"]>;
        required: true;
    };
    updateAttributes: {
        type: PropType<NodeViewProps["updateAttributes"]>;
        required: true;
    };
    deleteNode: {
        type: PropType<NodeViewProps["deleteNode"]>;
        required: true;
    };
    view: {
        type: PropType<NodeViewProps["view"]>;
        required: true;
    };
    innerDecorations: {
        type: PropType<NodeViewProps["innerDecorations"]>;
        required: true;
    };
    HTMLAttributes: {
        type: PropType<NodeViewProps["HTMLAttributes"]>;
        required: true;
    };
};
export interface VueNodeViewRendererOptions extends NodeViewRendererOptions {
    update: ((props: {
        oldNode: ProseMirrorNode;
        oldDecorations: readonly Decoration[];
        oldInnerDecorations: DecorationSource;
        newNode: ProseMirrorNode;
        newDecorations: readonly Decoration[];
        innerDecorations: DecorationSource;
        updateProps: () => void;
    }) => boolean) | null;
}
export declare function VueNodeViewRenderer(component: Component<NodeViewProps>, options?: Partial<VueNodeViewRendererOptions>): NodeViewRenderer;
//# sourceMappingURL=VueNodeViewRenderer.d.ts.map