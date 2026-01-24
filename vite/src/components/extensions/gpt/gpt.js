import { Extension } from '@tiptap/core'

function preparePrompt(editor, completionType = 'prompted') {
  var operation = "insert"
  var selectedText = window.getSelection().toString();

  let userPrompt = ""
  if (completionType === 'prompted') {
    var promptText = selectedText ? "Tell the AI how to modify the selection" : "Tell the AI what to add"
    userPrompt = prompt(promptText);

    if (!userPrompt) {
      return {}
    }
    operation = "insert"
  }

  if (!selectedText) {
    var anchor = editor.state.selection.anchor;
  }
  let fullText = editor.getText();

  if (completionType === 'invent') {
    //remove the trailing slash from the fullText
    fullText = fullText.substring(0, fullText.length - 1);
    operation = "insert"
  }

  console.log("Selected text: " + selectedText);
  // console.log("Anchor: " + anchor);
  console.log("Prompt: " + userPrompt);

  // split the fullText into two parts: before and after the selectedText, or before and after the anchor if selectedText is empty
  var prefix = fullText.substring(0, anchor);
  var suffix = fullText.substring(anchor + selectedText.length);

  //if prefix ends in a trailing slash, remove it
  if (prefix && prefix.endsWith("/")) {
    prefix = prefix.substring(0, prefix.length - 1);
  }

  // if there's selected text 
  if (selectedText.length > 0) {
    var completePrompt = `${prefix}\n>>>\n${selectedText}\n<<<\n${suffix}`
  } else {
    var completePrompt = `${prefix} >>><<< ${suffix}`
  }


  return { completePrompt, userPrompt, operation };
}

async function completeSelection(prompt, userPrompt, operation) {
  return fetch("/editor", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt: prompt,
      instruction: userPrompt,
      operation: operation
    }),
  })
}


export const Gpt = Extension.create({
  name: "gpt",

  addStorage() {
    return {
      loading: false,
    }
  },


  addKeyboardShortcuts() {
    return {
      'Mod-l': () => this.editor.commands.gpt(),
    }
  },

  addCommands() {
    return {
      gpt: (completionType) => ({ commands }) => {
        console.log("GPT command", completionType);

        this.storage.loading = true
        const { completePrompt, userPrompt, operation } = preparePrompt(this.editor, completionType)
        
        if (completePrompt) {
          completeSelection(completePrompt, userPrompt, operation)
            .then((response) => {
              if (!response.ok) {
                return Promise.reject(response);
              }
              return response.json();
            })
            .then((json) => {
              var response = json.text.trimStart()
              console.log("Response: ", response);
              this.editor.chain().focus().insertContent(response).run();
              this.storage.loading = false
            })
            .catch((response) => {
              this.storage.loading = false
              console.log(response);
              // Simple error notification
              alert("Sorry, something went wrong");
            })
            ;
        } else {
          this.storage.loading = false
        }
      },
    }
  }
})