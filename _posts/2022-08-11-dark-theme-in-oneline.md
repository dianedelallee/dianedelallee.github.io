---
title: Css dark-theme in root property
author: Diane Delallée
Date: 2022-08-11 13:06:31
categories: [Blog, css]
tags: [css, javascript]
---

# Discovery of color-scheme property

By putting the color-scheme property in your css, you can easily define the theme.

```css
:root {
  color-scheme: dark;
}
```

And by adding a bit of javascript you can easily change the theme of your website
````html
<div>
  <p>mon text</p>
</div>

<div>
  <button onclick="change_theme();">Change the theme</button>
</div>
````

```javascript
function change_theme(){
  var theme = getComputedStyle(document.body).getPropertyValue('color-scheme');
  var new_theme = (theme == 'dark') ? 'light': 'dark';
  document.documentElement.style.setProperty("color-scheme", new_theme);
}
```

## Codepen

You can find the full codepen [here](https://codepen.io/dianedelallee/pen/ZExjrrg)