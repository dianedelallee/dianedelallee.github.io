---
title: Play with Ruby
author: Diane Delallée 
date: 2021-06-30 13:32:00 +0100 
categories: [Blog, Ruby]
tags: [Ruby]
---

At the end of April, I was fired from my job due to economical decision inside the company. 
In less than once month I found a new job (at [QoQa](https://www.qoqa.ch/fr)) and need to start learning a new language: Ruby and a new framework: [Rails](https://rubyonrails.org/)


## What I have done to start leaning Ruby
To check how ruby works, I have followed the express tutorial on [ruby-lang](https://www.ruby-lang.org/fr/documentation/quickstart/).
This is a quick tutorial but if you came from Python this is enough to have a small idea on how it works.

To learn Rails Apis, I have followed the amazing tutorial from Alexandre Rousseau: [Api on Rails 6](https://github.com/madeindjs/api_on_rails)

## What I have already learnt

### Easier function for basic check 
Ruby and Rails are full of functions really useful and to understand.
example in ruby

```ruby
my_var ||= 4
```

versus the same in Python
```python
my_var = 4 if my_var is None else my_var
```

### Same function but with or without exception
In rails, you can call some functions and if you add an `!` and the end of the name it will raise an error, otherwise it will only return a boolean.
ex:
```ruby
MyModel.update(attr_1: value_1, attr_2: value2)   # will return false if this does not work
MyModel.update!(attr_1: value_1, attr_2: value2)   # will raise an exception if this does not work
```

### validation and check of controllers
With Rails you can easily define functions that are run before operations your model
for instance: 

```ruby
class MyModel < ApplicationRecord
  validates :attr_name, presence: true
  validate :method_name_for_more_complex_validation
    
  before_create :method_name_to_do_something_before_the_creation
  after_create :method_name_to_do_something_after_the_creation
  before_destroy :method_name_to_do_something_before_the_destroy
  after_destroy :method_name_to_do_something_after_the_destroy
  before_save :method_name_to_do_something_before_the_save
  after_save :method_name_to_do_something_after_the_save
  
  def method_name_to_do_something_before_the_creation
    puts 'my method that do something before the creation'
  end
  
  ... 
  
end
```

### Fixtures pour les tests
If you need to create specific object in your test database, this is really easy and convenient.

You need to create a file called `models.yml` (ex: `users.yml` for the User model) in `test/fixtures` folder, and define your object:
```yaml
# file users.yml
---
name_for_object_1:
  attr_1: value_1,
  attr_2: value_2,
  attr_3: value_3

name_for_object_2:
  attr_1: value_1,
  attr_2: value_2,
  attr_3: value_3
```

and in your test file, you can use this object by doing: 
```ruby
user_for_test = users(:name_for_object_1)
puts user_for_test.attr_1
assert_equal user_for_test.attr_1, 'your value'
```

## What was a bit difficult at first sight

### Parenthesis are not mandatory when you call a function
ex: 
```ruby
my_function(attr_1: value)
# is equal to 
my_function value

# or 
assert_equal user_for_test.attr_1, 'your value'
# is equal to
assert_equal(user_for_test.attr_1, 'your value')
```

### Rails magic
With Rails, there is a lot of implicit called, like the before_action/after_action. This is not always easy to understand what happens when you start coding in an existing project.

As Rails, provide a bunch of existing functions, this is also a bit complicated to have an overiew of what exist and can improve performance. 
I guess this is quite similar when you start to learn any new framework.

Let's see how my learning evolves in the next weeks.
