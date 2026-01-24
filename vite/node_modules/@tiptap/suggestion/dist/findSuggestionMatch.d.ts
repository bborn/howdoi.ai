import { Range } from '@tiptap/core';
import { ResolvedPos } from '@tiptap/pm/model';
export interface Trigger {
    char: string;
    allowSpaces: boolean;
    allowToIncludeChar: boolean;
    allowedPrefixes: string[] | null;
    startOfLine: boolean;
    $position: ResolvedPos;
}
export type SuggestionMatch = {
    range: Range;
    query: string;
    text: string;
} | null;
export declare function findSuggestionMatch(config: Trigger): SuggestionMatch;
//# sourceMappingURL=findSuggestionMatch.d.ts.map