import { embedResources } from './embed-resources';
import { toArray } from './util';
import { isDataUrl, resourceToDataURL } from './dataurl';
import { getMimeType } from './mimes';
async function embedBackground(clonedNode, options) {
    var _a;
    const background = (_a = clonedNode.style) === null || _a === void 0 ? void 0 : _a.getPropertyValue('background');
    if (background) {
        const cssString = await embedResources(background, null, options);
        clonedNode.style.setProperty('background', cssString, clonedNode.style.getPropertyPriority('background'));
    }
}
async function embedImageNode(clonedNode, options) {
    if (!(clonedNode instanceof HTMLImageElement && !isDataUrl(clonedNode.src)) &&
        !(clonedNode instanceof SVGImageElement &&
            !isDataUrl(clonedNode.href.baseVal))) {
        return;
    }
    const url = clonedNode instanceof HTMLImageElement
        ? clonedNode.src
        : clonedNode.href.baseVal;
    const dataURL = await resourceToDataURL(url, getMimeType(url), options);
    await new Promise((resolve, reject) => {
        clonedNode.onload = resolve;
        clonedNode.onerror = reject;
        const image = clonedNode;
        if (image.decode) {
            image.decode = resolve;
        }
        if (clonedNode instanceof HTMLImageElement) {
            clonedNode.srcset = '';
            clonedNode.src = dataURL;
        }
        else {
            clonedNode.href.baseVal = dataURL;
        }
    });
}
async function embedChildren(clonedNode, options) {
    const children = toArray(clonedNode.childNodes);
    const deferreds = children.map((child) => embedImages(child, options));
    await Promise.all(deferreds).then(() => clonedNode);
}
export async function embedImages(clonedNode, options) {
    if (clonedNode instanceof Element) {
        await embedBackground(clonedNode, options);
        await embedImageNode(clonedNode, options);
        await embedChildren(clonedNode, options);
    }
}
//# sourceMappingURL=embed-images.js.map