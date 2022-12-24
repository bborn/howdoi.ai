import { Node } from '@tiptap/core';
export interface HardBreakOptions {
    keepMarks: boolean;
    HTMLAttributes: Record<string, any>;
}
declare module '@tiptap/core' {
    interface Commands<ReturnType> {
        hardBreak: {
            /**
             * Add a hard break
             */
            setHardBreak: () => ReturnType;
        };
    }
}
export declare const HardBreak: Node<HardBreakOptions, any>;
