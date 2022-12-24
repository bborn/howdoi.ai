import { Extension } from '@tiptap/core';
export interface HistoryOptions {
    depth: number;
    newGroupDelay: number;
}
declare module '@tiptap/core' {
    interface Commands<ReturnType> {
        history: {
            /**
             * Undo recent changes
             */
            undo: () => ReturnType;
            /**
             * Reapply reverted changes
             */
            redo: () => ReturnType;
        };
    }
}
export declare const History: Extension<HistoryOptions, any>;
