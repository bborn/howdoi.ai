import { Node } from '@tiptap/core';
export interface BlockquoteOptions {
    HTMLAttributes: Record<string, any>;
}
declare module '@tiptap/core' {
    interface Commands<ReturnType> {
        blockQuote: {
            /**
             * Set a blockquote node
             */
            setBlockquote: () => ReturnType;
            /**
             * Toggle a blockquote node
             */
            toggleBlockquote: () => ReturnType;
            /**
             * Unset a blockquote node
             */
            unsetBlockquote: () => ReturnType;
        };
    }
}
export declare const inputRegex: RegExp;
export declare const Blockquote: Node<BlockquoteOptions, any>;
