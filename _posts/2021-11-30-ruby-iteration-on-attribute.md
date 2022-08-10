---
title: Ruby iteration on attributes
author: Diane Delallée 
date: 2021-11-30 11:12:00 +0100
categories: [Blog, ruby]
tags: [ruby, test]
---

When you are writing tests, you may need to update several attributes with the same value and, made some assertion on those.

Let's say you have an object `my_object`, that contains several kinds of prices: `[:standard_price, :discount_price, :minimum_price]`
and you want to iterate on those attributes.

Let's see several ways to write that:

## The Easy way

```ruby
a_list_of_price = ['9999999.99', '9999999.98', '99,99', '99.99', ' 99€', '99', '0']

ATTRIBUTES_TO_ITERATE_ON.each do |attribute|
  a_list_of_price.each do |price|
    my_object.standard_price = 9999999.99
    assert my_object.valid?
    
    my_object.discount_price = 9999999.99
    assert my_object.valid?
    
    my_object.minimum_price = 9999999.99
    assert my_object.valid?
  end
end
```

## A more flexible approach

```ruby
ATTRIBUTES_TO_ITERATE_ON = [:standard_price, :discount_price, :minimum_price].freeze
a_list_of_price = ['9999999.99', '9999999.98', '99,99', '99.99', ' 99€', '99', '0']

ATTRIBUTES_TO_ITERATE_ON.each do |attribute|
  a_list_of_price.each do |price|
    my_object.send("#{attribute}=", price.to_f)   # equivalent to my_object.standard_price = 9999999.99
    assert my_object.valid?   # or any other assertion
  end
end
```
