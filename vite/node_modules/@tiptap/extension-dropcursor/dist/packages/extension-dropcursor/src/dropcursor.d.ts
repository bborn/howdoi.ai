import { Extension } from '@tiptap/core';
export interface DropcursorOptions {
    color: string | undefined;
    width: number | undefined;
    class: string | undefined;
}
export declare const Dropcursor: Extension<DropcursorOptions, any>;
