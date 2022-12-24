import { Mark } from '@tiptap/core';
export interface StrikeOptions {
    HTMLAttributes: Record<string, any>;
}
declare module '@tiptap/core' {
    interface Commands<ReturnType> {
        strike: {
            /**
             * Set a strike mark
             */
            setStrike: () => ReturnType;
            /**
             * Toggle a strike mark
             */
            toggleStrike: () => ReturnType;
            /**
             * Unset a strike mark
             */
            unsetStrike: () => ReturnType;
        };
    }
}
export declare const inputRegex: RegExp;
export declare const pasteRegex: RegExp;
export declare const Strike: Mark<StrikeOptions, any>;
