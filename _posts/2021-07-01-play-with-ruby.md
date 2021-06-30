---
title: Play with SCSS 
author: Diane Delallée 
date: 2021-03-09 13:32:00 +0100 
categories: [Blog, css]
tags: [css]
---

As mentionned on the previous article, I decided to implement a small CSS library to become more familiar with SASS.

Why using SASS? I find it easier to read, and you can define some mixins qhich are similar to functions. It allowed you to to define styles that can be re-used throughout your stylesheet.
I prefere to use the SCSS convention by using brackets instead of using indentation.

Let's have a look of the definition of the variables.

## Define variables

```scss
// declaration of the variables
$my-wonderful-color: #F3D250;
$padding: 4px;

// use the variables in a element
body {
  color: $my-wonderful-color;
  padding: $padding;
}
```


## Condition
You can also define a condition to only apply style if the condition is valid.

```scss
$rounded-corners: false;

.button {
  border: 1px solid black;
  border-radius: if($rounded-corners, 5px, null);
}
```

## How to write clean code in SCSS

This is one of the reason I really enjoy SASS, you can nest element to have a context really understandable.

```scss
a {
  text-decoration: none;
  color: #FEC601;

  &:hover {    // the & is equal to write a:hover
    text-decoration: underline;
    font: {
      size: 16px;
      weight: bold;
    };
    cursor: pointer;
  }
}
```

## Use mixins

 A mixin lets you make groups of CSS declarations that you want to reuse throughout your site. You can even pass in values to make your mixin more flexible.

```scss
@mixin define_color_and_hover_effect($color: #FF0000) { // we define a default color
  text-decoration: none;
  color: $color;

  &:hover {
    text-decoration: underline;
    font: {
      size: 16px;
      weight: bold;
    };
    cursor: pointer;
  }
}

a {
  @include define_color_and_hover_effect(#FEC601);  // apply the style define in the mixin
}

.my-class-for-a-div {
  // we do not need to specify a param because our mixin have a default value if nothing is specify
  @include define_color_and_hover_effect();
}
```

## Extend

This is one of the most useful features of Sass. Using @extend lets you share a set of CSS properties from one selector to another.

```scss
.button {
  padding: 4px;
  text-decoration: none;
  &:active {
    box-shadow: 1px 1px 1px #666;
  }
}

.info-button {
  @extend .button;  // take everything we have in the .button class
  background-color: $middle-blue-green;
}
```

> As a rule of thumb, extends are the best option when you’re expressing a relationship between semantic 
> classes (or other semantic selectors) and mixins are necessary when you need to configure the styles using arguments


## Other useful functions

```scss
.darker-color {
  color: darken(#FEC601, 10)  // take a color and apply a darker filter on it
}

.lighter-color {
  color: lighten(#FEC601, 10) // take a color and apply a lighter filter on it
}

$border-dark: rgba($base-color, 0.88);  // if you want to define an opacity, you can specify you color variable instead of separated RGB value.
```

## How to use my SCSS file in my projecct.

First you need to transform your scss file into a css file. You can do that with this command line:
```shell
sass --watch path/to/your/style.scss path/to/your/style.css
```

Finally and as usual, you can import your css file in your html with
```html
  <link href="./path/to/your/style.css" rel="stylesheet">
```
