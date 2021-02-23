---
title: Mock and how to test the arguments
author: Diane Delallée
date: 2020-06-08 16:25:00 +0800
categories: [Blog, Mock]
tags: [mock, test]
---

In the case you need to check the parameters with a mock was called.

```python
from mock import patch

@patch('the_function_I_want_to_mock')
def test_vanilla_case(self, my_mock):
    call_to_the_function_which_contains_the_mock()

    # First I check if the function was called
    self.assertTrue(my_mock.called)
    
    # Now, I now that the function will called twice the mock and I want to check both
    args = my_mock.call_args_list[0][0]     # get the first call of the mock 
    self.assertEqual(args[0], 'value for the first parameter of the call')
    self.assertEqual(args[1], 'value for the second parameter of the call')
    self.assertEqual(args[2], 'value for the third parameter of the call')

    args = my_mock.call_args_list[1][0]     # get the second call of the mock
    self.assertEqual(args[0], 'value for the first parameter of the call')
    self.assertEqual(args[1], 'value for the second parameter of the call')
    self.assertEqual(args[2], 'value for the third parameter of the call')
```
