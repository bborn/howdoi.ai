import { Editor } from '@tiptap/core';
import { Component, h } from 'vue';
import { Editor as ExtendedEditor } from './Editor.js';
export interface VueRendererOptions {
    editor: Editor;
    props?: Record<string, any>;
}
type ExtendedVNode = ReturnType<typeof h> | null;
interface RenderedComponent {
    vNode: ExtendedVNode;
    destroy: () => void;
    el: Element | null;
}
/**
 * This class is used to render Vue components inside the editor.
 */
export declare class VueRenderer {
    renderedComponent: RenderedComponent;
    editor: ExtendedEditor;
    component: Component;
    el: Element | null;
    props: Record<string, any>;
    constructor(component: Component, { props, editor }: VueRendererOptions);
    get element(): Element | null;
    get ref(): any;
    renderComponent(): {
        vNode: import("vue").VNode<import("vue").RendererNode, import("vue").RendererElement, {
            [key: string]: any;
        }>;
        destroy: () => void;
        el: Element | null;
    };
    updateProps(props?: Record<string, any>): void;
    destroy(): void;
}
export {};
//# sourceMappingURL=VueRenderer.d.ts.map