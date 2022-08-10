---
title: Test Rails Validator with ActiveSupport::TestCase 
author: Diane Delallée 
date: 2021-09-29 11:12:00 +0100
categories: [Blog, ruby]
tags: [ruby, Rails, ActiveStorage]
---

I needed to write a [custom validator](https://guides.rubyonrails.org/active_record_validations.html) for one of our
Active Record. Once my validator written, I wanted to test it without called an existing model of the DB.

## Let's take an example for an easy case.

My Easy validator:

```ruby
class EmailValidator < ActiveModel::EachValidator
  def validate_each(record, attribute, value)
    unless value =~ /\A([^@\s]+)@((?:[-a-z0-9]+\.)+[a-z]{2,})\z/i
      record.errors[attribute] << (options[:message] || "is not an email")
    end
  end
end
```

and now your test for your validator:

```ruby
require 'test_helper'

class EmailValidatable
   include ActiveModel::Validations
   attr_accessor :email
   
   validates :email, email: true
end

class EmailValidatorTest < ActiveSupport::TestCase
   invalid_email_addresses = ['invalid email@example.com', 'invalid@ example.com', 'invalid@@example.com', 'invalid', 'invalid@example']
   
   def obj
      @obj ||= EmailValidatable.new
   end
   
   test 'should invalidate email address' do
      invalid_email_addresses.each do |email|
         obj.email = email
         assert_not obj.valid?
         assert_equal I18n.t('errors.messages.not_an_email_address'), obj.errors[:email][0], "no error message for invalid email address \"#{email}\""
      end
   end
   
   test 'should validate email address' do
     obj.email = FFaker::Internet.email
     assert obj.valid?
     assert obj.errors[:email].blank?
   end
end
```

## How to do that to test with Active Storage

Now I have a more complex validator that test only some caracteristic of our blob
for [active storage](https://edgeguides.rubyonrails.org/active_storage_overview.html).

I have something like that for my model and my validator:

```ruby 
class MyAmazingModel < ApplicationRecord
   has_one_attached :blob
   
   validates :blob, blob: true
   
   # some other validation
   after_save :do_something
   validates :other_attr, presence: true
   
   # other functions
   def amazing_function_1
      p 'oh yeah'
   end
   
   def amazing_function_2
      p 'oh noooo'
   end
end

class BlobValidator < ActiveModel::EachValidator
   def initialize(options)
      require 'mini_magick' unless defined?(MiniMagick)
      super(options)
   end
   
   def validate_each(record, attribute, _value)
      # do some stuff to validate the ratio, the dimension and the type of my blob 
   end
   
   private
   
   def function_to_check_the_ratio
      true
   end
   
   def function_to_check_the_dimension
      true
   end
      
   def function_to_check_the_type
      true
   end
end
```

This is how I have defined my test file for my BlobValidator. The goal is to not depend on existing model.

```ruby
require 'test_helper'

class BlobValidatable < ActiveStorage::Blob
  # To check that BlobValidator
  has_one_attached :blob

  validates :blob, blob: true
end

class BlobValidatableWithParam < ActiveStorage::Blob
  # To check BlobValidator with custom parameters. In the case the validator accept some parameters
  has_one_attached :blob

  validates :blob, blob: { aspect_ratio: :square, dimension: { width: 300, height: 300 }, type: ['image/png'] }
end

class BlobValidatorTest < ActiveSupport::TestCase
  def obj
    @obj ||= BlobValidatable.new
  end

  def obj_with_param
    @obj_with_param ||= BlobValidatableWithParam.new
  end
  
  test 'check blob validator invalid ratio' do
    # file should not have a ratio of 3:2 (default ratio of my BlobValidator)
    obj.blob.attach(io: File.open(Rails.root.join('path', 'to', 'my', 'invalid', 'file.jpg')), filename: 'file.jpg')
    assert obj.blob.attached?
    assert_not obj.valid?
    assert_includes obj.errors.messages[:blob], "Error message define in my BlobValidator"

    # file should not have a ratio of 1:1 (define in parameter of BlobValidatableWithParam)
    obj_with_param.blob.attach(io: File.open(Rails.root.join('path', 'to', 'my', 'invalid', 'file.jpg')), filename: 'file.jpg')
    assert obj_with_param.blob.attached?
    assert_not obj_with_param.valid?
    assert_includes obj_with_param.errors.messages[:blob], "Error message define in my BlobValidator"
  end
  
  test "check blob validator valid" do
    obj.blob.attach(io: File.open(Rails.root.join('path', 'to', 'my', 'valid', 'file.jpg')), filename: 'file.jpg')
    assert obj.blob.attached?
    assert obj.valid?

    obj_with_param.blob.attach(io: File.open(Rails.root.join('path', 'to', 'my', 'valid', 'file.jpg')), filename: 'file.png')
    assert obj_with_param.blob.attached?
    assert obj_with_param.valid?
  end
end
```

This is it, now you can create other tests to ensure all your validator is properly tested.
