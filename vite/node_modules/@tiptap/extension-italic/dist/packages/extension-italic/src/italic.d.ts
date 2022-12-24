import { Mark } from '@tiptap/core';
export interface ItalicOptions {
    HTMLAttributes: Record<string, any>;
}
declare module '@tiptap/core' {
    interface Commands<ReturnType> {
        italic: {
            /**
             * Set an italic mark
             */
            setItalic: () => ReturnType;
            /**
             * Toggle an italic mark
             */
            toggleItalic: () => ReturnType;
            /**
             * Unset an italic mark
             */
            unsetItalic: () => ReturnType;
        };
    }
}
export declare const starInputRegex: RegExp;
export declare const starPasteRegex: RegExp;
export declare const underscoreInputRegex: RegExp;
export declare const underscorePasteRegex: RegExp;
export declare const Italic: Mark<ItalicOptions, any>;
