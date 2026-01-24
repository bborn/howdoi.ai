import { Editor as CoreEditor, EditorOptions } from '@tiptap/core';
import { EditorState, Plugin, PluginKey } from '@tiptap/pm/state';
import { AppContext, ComponentInternalInstance, ComponentPublicInstance } from 'vue';
export type ContentComponent = ComponentInternalInstance & {
    ctx: ComponentPublicInstance;
};
export declare class Editor extends CoreEditor {
    private reactiveState;
    private reactiveExtensionStorage;
    contentComponent: ContentComponent | null;
    appContext: AppContext | null;
    constructor(options?: Partial<EditorOptions>);
    get state(): EditorState;
    get storage(): Record<string, any>;
    /**
     * Register a ProseMirror plugin.
     */
    registerPlugin(plugin: Plugin, handlePlugins?: (newPlugin: Plugin, plugins: Plugin[]) => Plugin[]): EditorState;
    /**
     * Unregister a ProseMirror plugin.
     */
    unregisterPlugin(nameOrPluginKey: string | PluginKey): EditorState | undefined;
}
//# sourceMappingURL=Editor.d.ts.map