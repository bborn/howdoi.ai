import { Mark } from '@tiptap/core';
export interface BoldOptions {
    HTMLAttributes: Record<string, any>;
}
declare module '@tiptap/core' {
    interface Commands<ReturnType> {
        bold: {
            /**
             * Set a bold mark
             */
            setBold: () => ReturnType;
            /**
             * Toggle a bold mark
             */
            toggleBold: () => ReturnType;
            /**
             * Unset a bold mark
             */
            unsetBold: () => ReturnType;
        };
    }
}
export declare const starInputRegex: RegExp;
export declare const starPasteRegex: RegExp;
export declare const underscoreInputRegex: RegExp;
export declare const underscorePasteRegex: RegExp;
export declare const Bold: Mark<BoldOptions, any>;
