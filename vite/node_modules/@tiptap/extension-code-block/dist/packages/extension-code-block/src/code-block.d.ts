import { Node } from '@tiptap/core';
export interface CodeBlockOptions {
    /**
     * Adds a prefix to language classes that are applied to code tags.
     * Defaults to `'language-'`.
     */
    languageClassPrefix: string;
    /**
     * Define whether the node should be exited on triple enter.
     * Defaults to `true`.
     */
    exitOnTripleEnter: boolean;
    /**
     * Define whether the node should be exited on arrow down if there is no node after it.
     * Defaults to `true`.
     */
    exitOnArrowDown: boolean;
    /**
     * Custom HTML attributes that should be added to the rendered HTML tag.
     */
    HTMLAttributes: Record<string, any>;
}
declare module '@tiptap/core' {
    interface Commands<ReturnType> {
        codeBlock: {
            /**
             * Set a code block
             */
            setCodeBlock: (attributes?: {
                language: string;
            }) => ReturnType;
            /**
             * Toggle a code block
             */
            toggleCodeBlock: (attributes?: {
                language: string;
            }) => ReturnType;
        };
    }
}
export declare const backtickInputRegex: RegExp;
export declare const tildeInputRegex: RegExp;
export declare const CodeBlock: Node<CodeBlockOptions, any>;
