import { Extension, ParentConfig } from '@tiptap/core';
declare module '@tiptap/core' {
    interface NodeConfig<Options, Storage> {
        /**
         * Allow gap cursor
         */
        allowGapCursor?: boolean | null | ((this: {
            name: string;
            options: Options;
            storage: Storage;
            parent: ParentConfig<NodeConfig<Options>>['allowGapCursor'];
        }) => boolean | null);
    }
}
export declare const Gapcursor: Extension<any, any>;
