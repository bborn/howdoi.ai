# Resize Textarea

**A simple resize textarea for Vue3.**

Inspired from vue-textarea-autosize (Works with Vue2)

## Installation

**Install the package using npm**

`npm i resize-textarea-vue3`

## Documentation

1. Create a new Vue instance
2. Import ResizeTextarea and use it

```js
import { createApp } from 'vue'
import ResizeTextarea from 'resize-textarea-vue3'

const app = createApp({
  /* root component options */
})
app.use(ResizeTextarea)
.mount('#app')

```
Available props:

| Props         | required      | type    | default |
| ------------- |:-------------:| -------:| -------:|
| placeholder   | no            | String  | Null    |
| rows          | no            | Number  | 2       |
| cols          | no            | Number  | 0       |
| minHeight     | no            | Number  | 50   px   |
| maxHeight (The content will be scrollable after set limit)     | no            | Number  | Null    |
| modelValue    | no            | String / Number  | Null    |
| autoResize  (The drag handle is disabled by default.)  | no            | Booolean| true    |

The default unit is (px)
```

```
Component simple usage example: 

```vue
<template>
    <div id="wrapper">
        <resize-textarea
        :placeholder="placeholder"
        :rows="2"
        :cols="4"
        :maxHeight="150"
        v-model="textValue">
        </resize-textarea>
    </div>
    <script>
    export default {
        data() {
            return {
                placeholder: "This is a test message",
                textValue: "reSize",
            }
        },
    }
    </script>
</template>
```

```

```
Component usage with update:modelValue event example:

```vue
<template>
    <div id="wrapper">
        <resize-textarea
        :placeholder="placeholder"
        :modelValue="textValue"
        @update:modelValue="(value)=>useUpdatedValue(value)"
        v-model="textValue">
        </resize-textarea>
    </div>
    <script>
    export default {
        data() {
            return {
                placeholder: "This is a test message",
                textValue: "reSize",
            }
        },
        methods: {
            useUpdatedValue(value) {
                //do something 
            }
        }
    }
    </script>
</template>
```
```

```
Component usage example with state management:

```vue
<template>
    <div id="wrapper">
        <resize-textarea
        :placeholder="placeholder"
        v-model="textValue">
        </resize-textarea>
    </div>
    <script>
    export default {
        data() {
            return {
                placeholder: "This is a test message",
            }
        },
        computed: {
            textValue: {
                get() {
                    return this.$store.state.textValue
                },
                set(v) {
                    this.$store.commit('UPDATE', v)
                }
            }
        }
    }
    </script>
</template>
```
