---
title: Abstract Factory in python
author: Diane Delallée
date: 2021-01-12 08:56:00 +0800
categories: [Blog, Python]
tags: [design pattern, python]
---

For 2021, I decided to implement several design pattern to become more friendly with them and start using in my projects.

## First implemented pattern: Abstract Factory


## Goal of the pattern

Abstract Factory is a creational design pattern that lets you produce families of related objects without specifying their concrete classes.
The idea is to abstract the creation of objects depending on business logic, platform choice, etc.

The client code calls the creation methods of a factory object instead of creating products directly with a constructor 
call (new operator). Since a factory corresponds to a single product variant, all its products will be compatible.

Client code works with factories and products only through their abstract interfaces. 
This lets the client code work with any product variants, created by the factory object. 
You just create a new concrete factory class and pass it to the client code.


## The code

You can fin the code relative to this pattern in [this Github repo](https://github.com/dianedelallee/pythonDesignPattern/tree/master/patterns/creational/abstract_factory)
