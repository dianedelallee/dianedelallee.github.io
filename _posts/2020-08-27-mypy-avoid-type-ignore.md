---
title: How to mock function without typing to not use type ignore
author: Diane Delallée
date: 2020-08-27 08:25:00 +0800
categories: [Blog, Python]
tags: [mypy, Python]
---


## Import only for mypy an internal module
If you need to import a module only for mypy, and do not want to create a circular dependency, you can do like that:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from internal_module import myModel


def my_function(entity: 'myModel') -> None:
    print(entity)
```
It will only import the internal_module if this fill if read for mypy. 
The quotes allow you to not import on the top of the file for the normal behaviour.

## Import for mypy an external module with no mypy

You are probably use an external library that do not use mypy. This is specially a problem if this library is use as a decorator

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeVar
    F = TypeVar('F')
    
    def the_function_without_mypy(f: F) -> F:
        pass

else: 
    from external_lib import the_function_without_mypy

@the_function_without_mypy
def my_function() -> None:
    # ... my amazing code ...
    pass

```
By doing that, you do not take into account the mypy of the decorator but it will only check the mypy of your function.

You can also do the same process if you import a class with some methods on it


```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeVar
    F = TypeVar('F')
    
    class TheModule:
        def function_not_typed(f: F) -> F:
            pass

else: 
    from external_lib import TheModule

@TheModule.function_not_typed
def my_function() -> None:
    # ... my amazing code ...
    pass
```

Last but not least, if you want to have a smaller import section, you can define all your "mocking" mypy function in a 
dedicated file.


```python
# the dedicated file called helper_mypy.py
from typing import TypeVar

F = TypeVar('F')

class TheModule:
    def function_not_typed(f: F) -> F:
        pass

```

```python
# the main file
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from <path/to/previous/file> import helper_mypy
else: 
    from external_lib import TheModule

@TheModule.function_not_typed
def my_function() -> None:
    # ... my amazing code ...
    pass
```

And that is it! You should now be able to not write `# type: ignore` near your decorator.