import { Node } from '@tiptap/core';
export declare type Level = 1 | 2 | 3 | 4 | 5 | 6;
export interface HeadingOptions {
    levels: Level[];
    HTMLAttributes: Record<string, any>;
}
declare module '@tiptap/core' {
    interface Commands<ReturnType> {
        heading: {
            /**
             * Set a heading node
             */
            setHeading: (attributes: {
                level: Level;
            }) => ReturnType;
            /**
             * Toggle a heading node
             */
            toggleHeading: (attributes: {
                level: Level;
            }) => ReturnType;
        };
    }
}
export declare const Heading: Node<HeadingOptions, any>;
