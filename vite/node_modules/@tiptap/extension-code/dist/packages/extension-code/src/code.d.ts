import { Mark } from '@tiptap/core';
export interface CodeOptions {
    HTMLAttributes: Record<string, any>;
}
declare module '@tiptap/core' {
    interface Commands<ReturnType> {
        code: {
            /**
             * Set a code mark
             */
            setCode: () => ReturnType;
            /**
             * Toggle inline code
             */
            toggleCode: () => ReturnType;
            /**
             * Unset a code mark
             */
            unsetCode: () => ReturnType;
        };
    }
}
export declare const inputRegex: RegExp;
export declare const pasteRegex: RegExp;
export declare const Code: Mark<CodeOptions, any>;
